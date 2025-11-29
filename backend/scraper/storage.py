import os
import json
from datetime import datetime
import pandas as pd


def _ensure_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def save_jobs_csv(jobs: list, path: str = "data/raw/raw_jobs.csv") -> dict:
    """Sauvegarde la liste de jobs dans un CSV. Fusionne avec le fichier existant si présent."""
    _ensure_dir(path)

    df_new = pd.DataFrame(jobs)
    if os.path.exists(path):
        try:
            df_old = pd.read_csv(path)
            df = pd.concat([df_old, df_new], ignore_index=True)
            df = df.drop_duplicates()
        except Exception:
            df = df_new
    else:
        df = df_new

    df.to_csv(path, index=False)
    return {"path": path, "count": len(df)}


def save_jobs_json(jobs: list, path: str = "data/raw/raw_jobs.json") -> dict:
    """Sauvegarde la liste de jobs dans un fichier JSON (écrase)."""
    _ensure_dir(path)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"scraped_at": datetime.utcnow().isoformat(), "jobs": jobs}, f, ensure_ascii=False, indent=2)
        return {"path": path, "count": len(jobs)}
    except Exception as e:
        return {"error": str(e)}


def load_jobs_csv(path: str = "data/raw/raw_jobs.csv") -> list:
    if not os.path.exists(path):
        return []
    try:
        df = pd.read_csv(path)
        return df.to_dict(orient="records")
    except Exception:
        return []
