#!/usr/bin/env python3
"""
RQ Worker for Inno Supps background jobs
"""

import os
import sys
from rq import Worker, Connection
from config import settings
from services.job_service import default_queue, high_queue, low_queue

def main():
    """Start RQ worker"""
    # Add current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Import all job modules to register them
    from jobs import email_jobs, calendar_jobs, call_jobs, research_jobs
    
    # Create worker
    with Connection():
        worker = Worker([default_queue, high_queue, low_queue])
        print(f"Starting worker for queues: default, high, low")
        print(f"Redis URL: {settings.redis_url}")
        print(f"Mock mode: {settings.mock_mode}")
        worker.work()

if __name__ == "__main__":
    main()
