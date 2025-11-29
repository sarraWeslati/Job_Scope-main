from fastapi import APIRouter
from scraper.scraper import scrape_jobs

router = APIRouter()

@router.post("/")
def run_scraping():
    result = scrape_jobs()
    return result