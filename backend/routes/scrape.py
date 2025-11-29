from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from backend.tasks import enqueue_job, get_job

router = APIRouter()


@router.post("/")
def enqueue_scraping(payload: Dict[str, Any] = None):
    """Enqueue a scraping job. Accepts optional JSON body with scraper params.

    Example body: {"query":"python","sources":["indeed"]}
    """
    try:
        job_id = enqueue_job(payload or {})
        return {"message": "Job enqueued", "job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{job_id}")
def scrape_status(job_id: str):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    # Return a copy with non-sensitive fields
    return {
        "id": job.get("id"),
        "status": job.get("status"),
        "created_at": job.get("created_at"),
        "started_at": job.get("started_at"),
        "finished_at": job.get("finished_at"),
        "result": job.get("result"),
        "error": job.get("error"),
    }