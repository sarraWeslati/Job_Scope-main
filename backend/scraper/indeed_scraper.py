import requests
from bs4 import BeautifulSoup
from datetime import datetime


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def scrape_indeed(query: str = "python", location: str = "", max_pages: int = 1) -> list:
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
        try:
            resp = requests.get(base_url, params=params, headers=HEADERS, timeout=10)
            resp.raise_for_status()
        except Exception:
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
                    browser = p.chromium.launch(headless=True)
                    page_ctx = browser.new_page()
                    params_str = f"?q={query.replace(' ', '+')}&l={location.replace(' ', '+')}&start={page * 10}"
                    url = base_url + params_str
                    page_ctx.goto(url, timeout=30000)
                    time.sleep(1)
                    html = page_ctx.content()
                    soup = BeautifulSoup(html, "html.parser")
                    cards = soup.select("div.jobsearch-SerpJobCard, .result, .job_seen_beacon")
                    if not cards:
                        cards = soup.select("a.tapItem, div.slider_item")
                    browser.close()
            except Exception:
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
