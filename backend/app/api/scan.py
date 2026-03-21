"""Scan job management endpoints."""

import uuid
from fastapi import APIRouter, Depends, Query
from app.core.security import get_current_user

router = APIRouter()

# In-memory job tracking (replace with Celery/Redis in production)
_scan_jobs = {}


@router.post("/trigger")
async def trigger_scan(
    categories: list[str] = Query(default=["Electronics", "Home & Kitchen"]),
    user_id: str = Depends(get_current_user),
):
    """Trigger a deal scanning job for selected categories."""
    job_id = str(uuid.uuid4())
    _scan_jobs[job_id] = {
        "job_id": job_id,
        "user_id": user_id,
        "categories": categories,
        "status": "queued",
        "progress": 0,
        "deals_found": 0,
    }
    return _scan_jobs[job_id]


@router.get("/status/{job_id}")
async def scan_status(job_id: str, user_id: str = Depends(get_current_user)):
    """Check the status of a scan job."""
    job = _scan_jobs.get(job_id)
    if not job:
        return {"job_id": job_id, "status": "not_found"}
    return job
