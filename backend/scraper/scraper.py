from datetime import datetime
import logging
import time
from typing import Any, Dict, List, Optional, Tuple

from .indeed_scraper import scrape_indeed
from .linkedin_scraper import scrape_linkedin
from .playwright_scraper import scrape_site_playwright
from .storage import save_jobs_csv, save_jobs_json

logger = logging.getLogger(__name__)


def scrape_jobs(
    query: str = "python",
    location: str = "",
    sources: Tuple[str, ...] = ("indeed", "linkedin"),
    max_pages: int = 1,
    max_jobs: int = 100,
    use_playwright: bool = False,
    headless: bool = True,
    proxies: Tuple[str, ...] = (),
    user_agents: Tuple[str, ...] = (),
    timeout: int = 30,
    retries: int = 1,
    save: bool = True,
    return_results: bool = True,
) -> Dict[str, Any]:
    """Orchestrate scraping across configured sources, deduplicate and optionally save.

    Returns a dict with metadata and (optionally) the job list.
    """

    jobs: List[Dict[str, Any]] = []

    def _record_meta(items: List[Dict[str, Any]], source_name: str) -> None:
        ts = datetime.utcnow().isoformat()
        for it in items:
            if isinstance(it, dict):
                it.setdefault("source", source_name)
                it.setdefault("scraped_at", ts)

    # Helper for retrying playwright requests (often more flaky)
    def _call_playwright(site: str) -> List[Dict[str, Any]]:
        last_exc: Optional[Exception] = None
        for attempt in range(1, max(1, retries) + 1):
            try:
                return list(scrape_site_playwright(
                    site=site,
                    query=query,
                    location=location,
                    max_jobs=max_jobs,
                    headless=headless,
                    proxies=list(proxies) if proxies else None,
                    user_agents=list(user_agents) if user_agents else None,
                    timeout=timeout,
                ))
            except TypeError:
                # Some versions of the playwright scraper may not accept timeout/headless
                try:
                    return list(scrape_site_playwright(site=site, query=query, location=location, max_jobs=max_jobs))
                except Exception as e:
                    last_exc = e
                    logger.exception("Playwright call failed (fallback) for %s (attempt %s)", site, attempt)
            except Exception as e:
                last_exc = e
                logger.exception("Playwright call failed for %s (attempt %s)", site, attempt)
            if attempt < retries:
                time.sleep(1)
        if last_exc:
            raise last_exc
        return []

    # Run scrapers
    if use_playwright:
        for site in sources:
            try:
                results = _call_playwright(site)
                _record_meta(results, site)
                jobs.extend(results)
            except Exception:
                logger.exception("Error scraping with Playwright for site: %s", site)
    else:
        if "indeed" in sources:
            try:
                results = list(
                    scrape_indeed(
                        query=query,
                        location=location,
                        max_pages=max_pages,
                        proxies=proxies,
                        user_agents=user_agents,
                        timeout=timeout,
                        headless=headless,
                    )
                )
                _record_meta(results, "indeed")
                jobs.extend(results)
            except Exception:
                logger.exception("Error scraping Indeed")

        if "linkedin" in sources:
            try:
                results = list(
                    scrape_linkedin(
                        query=query,
                        location=location,
                        max_pages=max_pages,
                        proxies=proxies,
                        user_agents=user_agents,
                        timeout=timeout,
                        headless=headless,
                    )
                )
                _record_meta(results, "linkedin")
                jobs.extend(results)
            except Exception:
                logger.exception("Error scraping LinkedIn")

    # Deduplicate by (title, company, location, source)
    unique: List[Dict[str, Any]] = []
    seen = set()
    for j in jobs:
        if not isinstance(j, dict):
            continue
        key = (
            j.get("title"),
            j.get("company"),
            j.get("location"),
            j.get("source"),
        )
        if key not in seen:
            seen.add(key)
            unique.append(j)

    csv_result = None
    json_result = None
    if save:
        try:
            csv_result = save_jobs_csv(unique)
        except Exception:
            logger.exception("Failed to save CSV of scraped jobs")
        try:
            json_result = save_jobs_json(unique)
        except Exception:
            logger.exception("Failed to save JSON of scraped jobs")

    out: Dict[str, Any] = {
        "message": f"{len(unique)} jobs scraped",
        "count": len(unique),
        "csv": csv_result,
        "json": json_result,
    }

    if return_results:
        out["jobs"] = unique

    return out