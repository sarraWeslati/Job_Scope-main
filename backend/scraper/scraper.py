from datetime import datetime
from .indeed_scraper import scrape_indeed
from .linkedin_scraper import scrape_linkedin
from .playwright_scraper import scrape_site_playwright
from .storage import save_jobs_csv, save_jobs_json


def scrape_jobs(query: str = "python", location: str = "", sources: tuple = ("indeed", "linkedin"), max_pages: int = 1, max_jobs: int = 100, use_playwright: bool = False):
    """
    Orchestrateur de scraping : lance les scrapers configurés, dé-duplique
    et sauvegarde les résultats dans `data/raw/raw_jobs.csv` (CSV) et JSON.

    - query: mot-clé de recherche
    - location: localisation (optionnel)
    - sources: tuple contenant 'indeed' et/ou 'linkedin'
    - max_pages: nombre de pages à récupérer par source
    """

    jobs = []

    # If Playwright requested, use the robust renderer-based scraper per site
    if use_playwright:
        for site in sources:
            try:
                jobs += scrape_site_playwright(site=site, query=query, location=location, max_jobs=max_jobs)
            except Exception:
                pass
    else:
        if "indeed" in sources:
            try:
                jobs += scrape_indeed(query=query, location=location, max_pages=max_pages)
            except Exception:
                pass

        if "linkedin" in sources:
            try:
                jobs += scrape_linkedin(query=query, location=location, max_pages=max_pages)
            except Exception:
                pass

    # Dé-duplication simple par (title, company, location)
    unique = []
    seen = set()
    for j in jobs:
        key = (j.get("title"), j.get("company"), j.get("location"))
        if key not in seen:
            seen.add(key)
            unique.append(j)

    # Sauvegarde
    csv_result = save_jobs_csv(unique)
    json_result = save_jobs_json(unique)

    return {
        "message": f"{len(unique)} jobs scraped and saved",
        "csv": csv_result,
        "json": json_result,
    }