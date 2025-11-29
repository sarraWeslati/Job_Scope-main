import pytest


def test_dedup_and_metadata(monkeypatch):
    """Verify that orchestration deduplicates by (title,company,location,source)
    and that metadata (`source`, `scraped_at`) is attached to each job.
    """
    from backend.scraper import scraper

    # jobs returned by indeed (two items with same title/company/location)
    base_job = {"title": "Dev", "company": "ACME", "location": "Remote", "url": "u1"}
    indeed_jobs = [base_job.copy(), base_job.copy()]

    # jobs returned by linkedin (same title/company/location but different source)
    linkedin_job = base_job.copy()

    # Monkeypatch the scraper functions used by orchestrator
    monkeypatch.setattr(scraper, "scrape_indeed", lambda **kwargs: indeed_jobs)
    monkeypatch.setattr(scraper, "scrape_linkedin", lambda **kwargs: [linkedin_job])

    out = scraper.scrape_jobs(query="dev", sources=("indeed", "linkedin"), max_pages=1, save=False, return_results=True)

    assert out["count"] == 2
    jobs = out.get("jobs")
    assert isinstance(jobs, list)
    # each job should have source and scraped_at
    for j in jobs:
        assert "source" in j
        assert "scraped_at" in j


def test_playwright_retries(monkeypatch):
    """Ensure the Playwright path retries on failure and eventually returns results."""
    from backend.scraper import scraper

    calls = {"n": 0}

    def flaky_playwright(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("transient")
        return [{"title": "A", "company": "B", "location": "C"}]

    monkeypatch.setattr(scraper, "scrape_site_playwright", flaky_playwright)

    out = scraper.scrape_jobs(query="x", sources=("indeed",), use_playwright=True, retries=2, save=False, return_results=True)

    # _call_playwright should have retried once then succeeded
    assert calls["n"] == 2
    assert out["count"] == 1
