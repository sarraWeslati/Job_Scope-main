from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def recommend_jobs():
    return {
        "recommendations": [
            {"title": "Data Scientist", "match_score": 85},
            {"title": "ML Engineer", "match_score": 79},
            {"title": "Backend Python Developer", "match_score": 74},
        ]
    }