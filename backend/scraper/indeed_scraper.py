import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Tuple

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def scrape_indeed(query: str = "python", location: str = "", max_pages: int = 1, proxies: Tuple[str, ...] = (), user_agents: Tuple[str, ...] = (), timeout: int = 10, headless: bool = True) -> List[dict]:
    """
    Scrape simple des résultats Indeed (approche par requêtes HTTP).
    Note: Indeed change fréquemment ses sélecteurs; ceci est un scrapper simple
    pour récupération d'exemple. Pour un scraping plus robuste, utiliser Playwright.
    """
    base_url = "https://www.indeed.com/jobs"
    jobs = []

    import time

    for page in range(max_pages):
        params = {"q": query, "l": location, "start": page * 10}
        resp = None
        headers = HEADERS.copy()
        if user_agents:
            headers["User-Agent"] = user_agents[0]
        req_proxies = None
        if proxies:
            # use the first proxy for requests calls
            p = proxies[0]
            req_proxies = {"http": p, "https": p}
        try:
            resp = requests.get(base_url, params=params, headers=headers, timeout=timeout, proxies=req_proxies)
            resp.raise_for_status()
        except Exception:
            logger.exception("Indeed HTTP request failed for page %s", page)
            resp = None

        soup = BeautifulSoup(resp.text, "html.parser") if resp is not None else None

        # sélecteurs variés pour s'adapter aux versions
        cards = []
        if soup is not None:
            cards = soup.select("div.jobsearch-SerpJobCard, .result, .job_seen_beacon")
            if not cards:
                # alternative: recherche d'éléments standards
                cards = soup.select("a.tapItem, div.slider_item")

        # Si aucune carte trouvée avec requests, essayer Playwright pour rendre la page
        if not cards:
            try:
                from playwright.sync_api import sync_playwright

                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=headless)
                    page_ctx = browser.new_page()
                    if user_agents:
                        page_ctx.set_extra_http_headers({"User-Agent": user_agents[0]})
                    params_str = f"?q={query.replace(' ', '+')}&l={location.replace(' ', '+')}&start={page * 10}"
                    url = base_url + params_str
                    # playwright timeout is in ms
                    page_ctx.goto(url, timeout=timeout * 1000)
                    time.sleep(1)
                    html = page_ctx.content()
                    soup = BeautifulSoup(html, "html.parser")
                    cards = soup.select("div.jobsearch-SerpJobCard, .result, .job_seen_beacon")
                    if not cards:
                        cards = soup.select("a.tapItem, div.slider_item")
                    browser.close()
            except Exception:
                logger.exception("Playwright fallback failed for Indeed page %s", page)
                cards = []

        for card in cards:
            title_el = card.select_one("h2.jobTitle, h2 > a, .jobTitle a, .jobTitle")
            title = title_el.get_text(strip=True) if title_el else None

            company_el = card.select_one(".companyName, .company")
            company = company_el.get_text(strip=True) if company_el else None

            loc_el = card.select_one(".companyLocation, .location")
            location_text = loc_el.get_text(strip=True) if loc_el else None

            summary_el = card.select_one(".summary, .job-snippet")
            summary = summary_el.get_text(strip=True) if summary_el else None

            link = None
            a = card.select_one("a")
            if a and a.get("href"):
                href = a.get("href")
                if href.startswith("/"):
                    link = "https://www.indeed.com" + href
                else:
                    link = href

            jobs.append({
                "title": title,
                "company": company,
                "location": location_text,
                "summary": summary,
                "url": link,
                "source": "indeed",
                "scraped_at": datetime.utcnow().isoformat(),
            })

    return jobs
