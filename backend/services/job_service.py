"""
Job orchestration service using RQ (Redis Queue)
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Callable
from rq import Queue, Worker, Connection
from rq.job import Job
from rq_scheduler import Scheduler
from backend.config import settings
from backend.services.redis_cache import cache
from backend.database import Job as JobModel, JobStatus, get_db
from sqlalchemy.orm import Session

# Initialize Redis connection
import redis
redis_conn = redis.from_url(settings.redis_url)

# Create queues
default_queue = Queue('default', connection=redis_conn)
high_queue = Queue('high', connection=redis_conn)
low_queue = Queue('low', connection=redis_conn)

# Create scheduler
scheduler = Scheduler(connection=redis_conn)

class JobService:
    def __init__(self):
        self.queues = {
            'default': default_queue,
            'high': high_queue,
            'low': low_queue
        }
    
    def job(self, queue_name: str = "default", timeout: int = 300, retry: int = 3):
        """Decorator to register a function as a job"""
        def decorator(func: Callable):
            def wrapper(*args, **kwargs):
                return self.enqueue_job(
                    func.__name__,
                    func,
                    args,
                    kwargs,
                    queue_name,
                    timeout,
                    retry
                )
            return wrapper
        return decorator
    
    def enqueue_job(
        self,
        job_type: str,
        func: Callable,
        args: tuple,
        kwargs: dict,
        queue_name: str = "default",
        timeout: int = 300,
        retry: int = 3,
        workspace_id: Optional[str] = None,
        delay: Optional[timedelta] = None
    ) -> str:
        """Enqueue a job"""
        # Create dedupe key for idempotency
        payload_str = json.dumps({
            "func": func.__name__,
            "args": args,
            "kwargs": kwargs
        }, sort_keys=True)
        dedupe_key = hashlib.md5(payload_str.encode()).hexdigest()
        
        # Check if job already exists
        if workspace_id:
            existing_job = self.get_job_by_dedupe_key(dedupe_key, workspace_id)
            if existing_job and existing_job.status in [JobStatus.QUEUED, JobStatus.RUNNING]:
                return str(existing_job.id)
        
        # Create job record in database
        db = next(get_db())
        try:
            job_record = JobModel(
                workspace_id=workspace_id or "system",
                type=job_type,
                payload_json={
                    "func": func.__name__,
                    "args": args,
                    "kwargs": kwargs,
                    "dedupe_key": dedupe_key
                },
                status=JobStatus.QUEUED,
                attempts=0
            )
            db.add(job_record)
            db.commit()
            db.refresh(job_record)
            job_id = str(job_record.id)
        except Exception as e:
            db.rollback()
            print(f"Error creating job record: {e}")
            return None
        finally:
            db.close()
        
        # Enqueue in Redis
        try:
            queue = self.queues.get(queue_name, default_queue)
            
            if delay:
                # Schedule for later
                scheduler.enqueue_in(
                    delay,
                    self._execute_job,
                    job_id,
                    func,
                    args,
                    kwargs,
                    timeout=timeout,
                    job_timeout=timeout,
                    retry=retry
                )
            else:
                # Execute immediately
                queue.enqueue(
                    self._execute_job,
                    job_id,
                    func,
                    args,
                    kwargs,
                    timeout=timeout,
                    job_timeout=timeout,
                    retry=retry
                )
            
            return job_id
        except Exception as e:
            print(f"Error enqueueing job: {e}")
            # Update job status to failed
            self.update_job_status(job_id, JobStatus.FAILED, str(e))
            return None
    
    def _execute_job(self, job_id: str, func: Callable, args: tuple, kwargs: dict):
        """Execute a job and update status"""
        # Update job status to running
        self.update_job_status(job_id, JobStatus.RUNNING)
        
        try:
            # Execute the function
            result = func(*args, **kwargs)
            
            # Update job status to succeeded
            self.update_job_status(job_id, JobStatus.SUCCEEDED)
            
            return result
        except Exception as e:
            # Update job status to failed
            self.update_job_status(job_id, JobStatus.FAILED, str(e))
            raise e
    
    def update_job_status(self, job_id: str, status: JobStatus, error: Optional[str] = None):
        """Update job status in database"""
        db = next(get_db())
        try:
            job = db.query(JobModel).filter(JobModel.id == job_id).first()
            if job:
                job.status = status
                job.attempts += 1
                if error:
                    job.last_error = error
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error updating job status: {e}")
        finally:
            db.close()
    
    def get_job_by_dedupe_key(self, dedupe_key: str, workspace_id: str) -> Optional[JobModel]:
        """Get job by dedupe key for idempotency"""
        db = next(get_db())
        try:
            return db.query(JobModel).filter(
                JobModel.workspace_id == workspace_id,
                JobModel.payload_json['dedupe_key'].astext == dedupe_key
            ).first()
        finally:
            db.close()
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job status"""
        db = next(get_db())
        try:
            job = db.query(JobModel).filter(JobModel.id == job_id).first()
            if job:
                return {
                    "id": str(job.id),
                    "type": job.type,
                    "status": job.status.value,
                    "attempts": job.attempts,
                    "last_error": job.last_error,
                    "created_at": job.created_at.isoformat(),
                    "updated_at": job.updated_at.isoformat()
                }
            return None
        finally:
            db.close()
    
    def get_workspace_jobs(self, workspace_id: str, limit: int = 100) -> list[Dict[str, Any]]:
        """Get jobs for a workspace"""
        db = next(get_db())
        try:
            jobs = db.query(JobModel).filter(
                JobModel.workspace_id == workspace_id
            ).order_by(JobModel.created_at.desc()).limit(limit).all()
            
            return [
                {
                    "id": str(job.id),
                    "type": job.type,
                    "status": job.status.value,
                    "attempts": job.attempts,
                    "last_error": job.last_error,
                    "created_at": job.created_at.isoformat(),
                    "updated_at": job.updated_at.isoformat()
                }
                for job in jobs
            ]
        finally:
            db.close()
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a job"""
        try:
            # Try to cancel in Redis
            for queue in self.queues.values():
                job = queue.fetch_job(job_id)
                if job:
                    job.cancel()
                    break
            
            # Update status in database
            self.update_job_status(job_id, JobStatus.FAILED, "Cancelled by user")
            return True
        except Exception as e:
            print(f"Error cancelling job: {e}")
            return False
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue statistics"""
        stats = {}
        for name, queue in self.queues.items():
            stats[name] = {
                "queued": len(queue),
                "failed": len(queue.failed_job_registry),
                "started": len(queue.started_job_registry),
                "finished": len(queue.finished_job_registry)
            }
        return stats

# Global job service instance
job_service = JobService()

# Job decorators
def job(queue_name: str = "default", timeout: int = 300, retry: int = 3):
    """Decorator to register a function as a job"""
    return job_service.job(queue_name, timeout, retry)
