import pandas as pd
import os

RAW_PATH = "data/raw/raw_jobs.csv"
CLEANED_PATH = "data/cleaned/cleaned_jobs.csv"

def clean_jobs():
    """
    Nettoie et normalise les données scrappées :
    - Supprime les doublons
    - Supprime les lignes vides
    - Normalise les colonnes (titre, entreprise, localisation)
    - Sauvegarde dans cleaned_jobs.csv
    """

    if not os.path.exists(RAW_PATH):
        return {"error": f"{RAW_PATH} introuvable. Lance d'abord le scraping."}

    df = pd.read_csv(RAW_PATH)

    # Supprimer les doublons
    df = df.drop_duplicates()

    # Supprimer les lignes vides
    df = df.dropna(how="all")

    # Normaliser les colonnes
    if "title" in df.columns:
        df["title"] = df["title"].str.strip().str.title()

    if "company" in df.columns:
        df["company"] = df["company"].str.strip().str.upper()

    if "location" in df.columns:
        df["location"] = df["location"].str.strip().str.capitalize()

    # Sauvegarde
    os.makedirs(os.path.dirname(CLEANED_PATH), exist_ok=True)
    df.to_csv(CLEANED_PATH, index=False)

    return {"message": f"{len(df)} jobs nettoyés et stockés dans {CLEANED_PATH}"}