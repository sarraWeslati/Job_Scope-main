from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from routes.scrape import router as scrape_router
from routes.recommend import router as recommend_router
from routes.clean import router as clean_router

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

# ---------------------------
# ROUTE 1 : INSIGHTS (BI)
# ---------------------------
@app.get("/insights")
def get_insights():
    return {
        "top_skills": [
            {"skill": "Python", "count": 120},
            {"skill": "Machine Learning", "count": 95},
            {"skill": "React", "count": 80},
            {"skill": "SQL", "count": 70},
        ]
    }

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