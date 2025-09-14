"""
Job management routes for Inno Supps
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from services.job_service import job_service
from services.auth_service import auth_service
from routes.auth import get_current_user
from database import User

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/status/{job_id}")
async def get_job_status(job_id: str, current_user: User = Depends(get_current_user)):
    """Get status of a specific job"""
    status = job_service.get_job_status(job_id)
    if not status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return status

@router.get("/workspace")
async def get_workspace_jobs(
    workspace_id: str,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """Get all jobs for a workspace"""
    # Verify user has access to workspace
    if not auth_service.can_read(current_user.id, workspace_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to workspace"
        )
    
    jobs = job_service.get_workspace_jobs(workspace_id, limit)
    return {"jobs": jobs}

@router.post("/cancel/{job_id}")
async def cancel_job(job_id: str, current_user: User = Depends(get_current_user)):
    """Cancel a job"""
    success = job_service.cancel_job(job_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to cancel job"
        )
    return {"message": "Job cancelled successfully"}

@router.get("/queue-stats")
async def get_queue_stats(current_user: User = Depends(get_current_user)):
    """Get queue statistics"""
    stats = job_service.get_queue_stats()
    return {"queue_stats": stats}

@router.post("/email/ingest")
async def trigger_email_ingest(
    workspace_id: str,
    email_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Trigger email ingestion job"""
    # Verify user has access to workspace
    if not auth_service.can_write(current_user.id, workspace_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to workspace"
        )
    
    from jobs.email_jobs import ingest_email
    job_id = job_service.enqueue_job(
        "ingest_email",
        ingest_email,
        (workspace_id, email_data),
        {},
        workspace_id=workspace_id
    )
    
    return {"job_id": job_id, "message": "Email ingestion job queued"}

@router.post("/research/niche")
async def trigger_niche_research(
    workspace_id: str,
    research_inputs: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Trigger niche research job"""
    # Verify user has access to workspace
    if not auth_service.can_write(current_user.id, workspace_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to workspace"
        )
    
    from jobs.research_jobs import run_niche_research
    job_id = job_service.enqueue_job(
        "run_niche_research",
        run_niche_research,
        (workspace_id, research_inputs),
        {},
        workspace_id=workspace_id
    )
    
    return {"job_id": job_id, "message": "Niche research job queued"}

@router.post("/growth-plan")
async def trigger_growth_plan(
    workspace_id: str,
    plan_inputs: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Trigger growth plan creation job"""
    # Verify user has access to workspace
    if not auth_service.can_write(current_user.id, workspace_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to workspace"
        )
    
    from backend.jobs.research_jobs import create_growth_plan
    job_id = job_service.enqueue_job(
        "create_growth_plan",
        create_growth_plan,
        (workspace_id, plan_inputs),
        {},
        workspace_id=workspace_id
    )
    
    return {"job_id": job_id, "message": "Growth plan job queued"}

@router.post("/calls/transcribe")
async def trigger_call_transcription(
    workspace_id: str,
    recording_url: str,
    prospect_id: str = None,
    current_user: User = Depends(get_current_user)
):
    """Trigger call transcription job"""
    # Verify user has access to workspace
    if not auth_service.can_write(current_user.id, workspace_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to workspace"
        )
    
    from backend.jobs.call_jobs import transcribe_and_analyze_call
    job_id = job_service.enqueue_job(
        "transcribe_and_analyze_call",
        transcribe_and_analyze_call,
        (workspace_id, recording_url, prospect_id),
        {},
        workspace_id=workspace_id
    )
    
    return {"job_id": job_id, "message": "Call transcription job queued"}
