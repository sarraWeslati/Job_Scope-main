import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from typing import List, Tuple

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def scrape_linkedin(query: str = "python", location: str = "", max_pages: int = 1, proxies: Tuple[str, ...] = (), user_agents: Tuple[str, ...] = (), timeout: int = 10, headless: bool = True) -> List[dict]:
    """
    Tentative de scraping LinkedIn via requêtes simples. LinkedIn bloque souvent
    les requêtes non-rendered; si la méthode retourne peu ou pas de résultats,
    passez à Playwright (déjà présent dans `requirements.txt`).
    """
    jobs = []

    # LinkedIn change souvent son front. Voici une tentative simple sur la page publique.
    base_url = "https://www.linkedin.com/jobs/search/"

    for page in range(max_pages):
        params = {"keywords": query, "location": location, "start": page * 25}
        resp = None
        headers = HEADERS.copy()
        if user_agents:
            headers["User-Agent"] = user_agents[0]
        req_proxies = None
        if proxies:
            p = proxies[0]
            req_proxies = {"http": p, "https": p}
        try:
            resp = requests.get(base_url, params=params, headers=headers, timeout=timeout, proxies=req_proxies)
            resp.raise_for_status()
        except Exception:
            logger.exception("LinkedIn HTTP request failed for page %s", page)
            resp = None

        soup = BeautifulSoup(resp.text, "html.parser") if resp is not None else None

        cards = []
        if soup is not None:
            cards = soup.select(".job-card-container, .result-card, li")
            if not cards:
                cards = soup.select(".base-card")

        # Fallback Playwright si rien trouvé
        if not cards:
            try:
                from playwright.sync_api import sync_playwright

                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=headless)
                    page_ctx = browser.new_page()
                    if user_agents:
                        page_ctx.set_extra_http_headers({"User-Agent": user_agents[0]})
                    params_str = f"?keywords={query.replace(' ', '+')}&location={location.replace(' ', '+')}&start={page * 25}"
                    url = base_url + params_str
                    page_ctx.goto(url, timeout=timeout * 1000)
                    time.sleep(1)
                    html = page_ctx.content()
                    soup = BeautifulSoup(html, "html.parser")
                    cards = soup.select(".job-card-container, .result-card, li")
                    if not cards:
                        cards = soup.select(".base-card")
                    browser.close()
            except Exception:
                logger.exception("Playwright fallback failed for LinkedIn page %s", page)
                cards = []

        for card in cards:
            title_el = card.select_one("h3, .base-search-card__title, .job-card-list__title")
            title = title_el.get_text(strip=True) if title_el else None

            company_el = card.select_one("h4, .base-search-card__subtitle, .job-card-container__company-name")
            company = company_el.get_text(strip=True) if company_el else None

            loc_el = card.select_one(".job-card-container__metadata-item, .job-result-card__location")
            location_text = loc_el.get_text(strip=True) if loc_el else None

            link_el = card.select_one("a")
            link = None
            if link_el and link_el.get("href"):
                link = link_el.get("href")

            jobs.append({
                "title": title,
                "company": company,
                "location": location_text,
                "url": link,
                "source": "linkedin",
                "scraped_at": datetime.utcnow().isoformat(),
            })

    return jobs
