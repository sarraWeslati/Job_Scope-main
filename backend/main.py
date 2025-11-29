from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from routes.scrape import router as scrape_router
from routes.recommend import router as recommend_router
from routes.clean import router as clean_router
from typing import List, Dict
import json
import re
import os

# ⚠️ Définir l'app AVANT d'utiliser include_router
app = FastAPI()

# Inclure les routes
app.include_router(scrape_router, prefix="/api/scrape")
app.include_router(recommend_router, prefix="/api/recommend")
app.include_router(clean_router, prefix="/api/clean")

# Autoriser le frontend Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _load_saved_jobs(path: str = "data/raw/raw_jobs.json") -> List[Dict]:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
            return payload.get("jobs", [])
    except Exception:
        return []


def _top_tokens_from_titles(jobs: List[Dict], top_n: int = 8) -> List[Dict]:
    # Very simple tokenizer — split on non-word, lowercase, filter stopwords and short tokens
    stopwords = {
        "and",
        "or",
        "the",
        "a",
        "an",
        "senior",
        "junior",
        "engineer",
        "developer",
        "software",
        "manager",
        "senior",
        "lead",
        "fullstack",
        "early",
        "career",
        "python",
    }
    counts = {}
    for j in jobs:
        title = j.get("title") or ""
        tokens = re.split(r"[^A-Za-z]+", title)
        for t in tokens:
            t = t.strip().lower()
            if not t or len(t) < 3:
                continue
            if t in stopwords:
                continue
            counts[t] = counts.get(t, 0) + 1

    items = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [{"name": k.title(), "count": v} for k, v in items]


# ---------------------------
# ROUTE 1 : INSIGHTS (BI)
# ---------------------------
@app.get("/insights")
def get_insights():
    jobs = _load_saved_jobs()
    skills = _top_tokens_from_titles(jobs)
    # Provide `skills` key expected by frontend SkillChart
    return {"skills": skills}

# ---------------------------
# ROUTE 2 : JOBS LIST
# ---------------------------
@app.get("/jobs")
def get_jobs():
    return [
        {"title": "Fullstack Developer", "company": "Tech Vision", "location": "Tunis"},
        {"title": "Data Scientist", "company": "AI Labs", "location": "Sousse"},
        {"title": "React Frontend Engineer", "company": "Webify", "location": "Sfax"},
    ]

# ---------------------------
# ROUTE 3 : SCRAPING (fake)
# ---------------------------
@app.get("/scrape")
def scrape_data():
    return {"message": "Scraping done successfully (fake)"}

# ---------------------------
# ROUTE 4 : MATCH (Upload CV)
# ---------------------------
@app.post("/match")
async def match_cv(file: UploadFile = File(...)):
    return {
        "recommendations": [
            {"title": "Data Scientist", "match_score": 85},
            {"title": "ML Engineer", "match_score": 79},
            {"title": "Backend Python Developer", "match_score": 74},
        ]
    }