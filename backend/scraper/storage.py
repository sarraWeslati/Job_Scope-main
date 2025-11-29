import os
import json
import csv
from datetime import datetime
from typing import Iterable


def _ensure_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def save_jobs_csv(jobs: Iterable[dict], path: str = "data/raw/raw_jobs.csv") -> dict:
    """
    Sauvegarde la liste de jobs dans un CSV en mode streaming/append.
    - Si le fichier existe, on ajoute les nouvelles lignes en évitant d'écraser.
    - `jobs` peut être une liste ou un itérable.
    """
    _ensure_dir(path)

    # Normaliser en liste pour inspecter les clés si nécessaire
    rows = list(jobs)
    if not rows:
        return {"path": path, "count": 0}

    fieldnames = list({k for r in rows for k in r.keys()})

    write_header = not os.path.exists(path)

    try:
        with open(path, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")
            if write_header:
                writer.writeheader()
            for r in rows:
                writer.writerow(r)
        # Count lines (fast enough for moderate files)
        try:
            with open(path, "r", encoding="utf-8") as f:
                count = sum(1 for _ in f) - 1
                if count < 0:
                    count = 0
        except Exception:
            count = len(rows)
        return {"path": path, "count": count}
    except Exception as e:
        return {"error": str(e)}


def save_jobs_json(jobs: list, path: str = "data/raw/raw_jobs.json") -> dict:
    """Sauvegarde la liste de jobs dans un fichier JSON (écrase)."""
    _ensure_dir(path)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"scraped_at": datetime.utcnow().isoformat(), "jobs": list(jobs)}, f, ensure_ascii=False, indent=2)
        return {"path": path, "count": len(jobs)}
    except Exception as e:
        return {"error": str(e)}


def load_jobs_csv(path: str = "data/raw/raw_jobs.csv") -> list:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [row for row in reader]
    except Exception:
        return []
