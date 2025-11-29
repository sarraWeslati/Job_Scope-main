import json
from scraper.playwright_scraper import scrape_site_playwright
from scraper.storage import save_jobs_csv, save_jobs_json
from scraper.config import USER_AGENTS, PROXIES


def main():
    all_jobs = []
    sites = ("indeed", "linkedin")
    for site in sites:
        print(f"Scraping site={site} (max 30, headful)...")
        jobs = scrape_site_playwright(site=site, query="python", location="", max_jobs=50, headless=False, proxies=PROXIES if PROXIES else None, user_agents=USER_AGENTS)
        print(f"  -> collected {len(jobs)} jobs from {site}")
        all_jobs.extend(jobs)

    # Save combined results
    csv_res = save_jobs_csv(all_jobs)
    json_res = save_jobs_json(all_jobs)

    summary = {
        "total": len(all_jobs),
        "per_site": {s: len([j for j in all_jobs if j.get("source") == s]) for s in sites},
        "csv": csv_res,
        "json": json_res,
    }

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
