from fastapi import APIRouter
from scraper.cleaner import clean_jobs

router = APIRouter()

@router.post("/")
def run_cleaning():
    result = clean_jobs()
    return result