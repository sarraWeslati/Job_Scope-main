import time
import random
from datetime import datetime
from typing import List

from playwright.sync_api import sync_playwright


def _random_sleep(min_s=0.5, max_s=1.5):
    time.sleep(random.uniform(min_s, max_s))


def _extract_text_or_none(el):
    try:
        return el.inner_text().strip()
    except Exception:
        return None


def scrape_site_playwright(site: str, query: str = "python", location: str = "", max_jobs: int = 100, headless: bool = True) -> List[dict]:
    """
    Generic Playwright scraper for Indeed and LinkedIn search pages.

    - site: 'indeed' or 'linkedin'
    - query, location: search parameters
    - max_jobs: number of offers to collect (stop early if exhausted)
    """

    results = []
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        start = 0
        increment = 10 if site == "indeed" else 25

        while len(results) < max_jobs:
            if site == "indeed":
                url = f"https://www.indeed.com/jobs?q={query.replace(' ', '+')}&l={location.replace(' ', '+')}&start={start}"
                card_selectors = ["a.tapItem", "div.job_seen_beacon", "div.jobsearch-SerpJobCard"]
            elif site == "linkedin":
                url = f"https://www.linkedin.com/jobs/search?keywords={query.replace(' ', '+')}&location={location.replace(' ', '+')}&start={start}"
                card_selectors = [".base-card", "li.result-card", ".jobs-search-results__list-item"]
            else:
                break

            try:
                page.goto(url, timeout=30000)
            except Exception:
                break

            # scroll a bit to trigger lazy loading
            for _ in range(3):
                page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                _random_sleep(0.3, 1.0)

            cards = []
            for sel in card_selectors:
                locs = page.locator(sel)
                try:
                    count = locs.count()
                except Exception:
                    count = 0
                if count:
                    for i in range(count):
                        try:
                            cards.append(locs.nth(i))
                        except Exception:
                            continue
                    break

            if not cards:
                # no more results or page structure changed
                break

            for c in cards:
                try:
                    title_el = c.locator("h2, h3, .jobTitle, .base-search-card__title")
                    title = _extract_text_or_none(title_el) if title_el else None

                    company_el = c.locator(".companyName, .company, .base-search-card__subtitle, h4")
                    company = _extract_text_or_none(company_el) if company_el else None

                    loc_el = c.locator(".companyLocation, .job-result-card__location, .job-card-container__metadata-item")
                    location_text = _extract_text_or_none(loc_el) if loc_el else None

                    link_el = c.locator("a")
                    url_link = None
                    try:
                        url_link = link_el.get_attribute("href") if link_el else None
                    except Exception:
                        url_link = None

                    key = (title, company, location_text)
                    if key in seen:
                        continue
                    seen.add(key)

                    results.append({
                        "title": title,
                        "company": company,
                        "location": location_text,
                        "url": url_link,
                        "source": site,
                        "scraped_at": datetime.utcnow().isoformat(),
                    })

                    if len(results) >= max_jobs:
                        break
                except Exception:
                    continue

            start += increment
            _random_sleep(0.5, 1.5)

        browser.close()

    return results
