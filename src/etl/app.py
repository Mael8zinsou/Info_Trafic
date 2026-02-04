import os
import glob
import pandas as pd
from pathlib import Path
#import logging
from src.utils.log_utils import get_logger

# # Config logs
# LOG_DIR = "/app/logs"

ROOT_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT_DIR / "logs"
DATA_DIR = ROOT_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

from datetime import datetime
import shutil

logger = get_logger("etl", LOG_DIR / "etl.log")

def etl_process():
    env = os.environ.get("ENV", "preprod").lower()
    if env == "prod":
        source_dir = DATA_DIR / "raw"
    elif env == "preprod":
        source_dir = DATA_DIR / "samples"
    else:
        logger.warning(f"ENV non reconnu ({env}), utilisation de preprod par défaut")
        source_dir = DATA_DIR / "samples"

    csv_files = glob.glob(str(source_dir / "*.csv"))
    if not csv_files:
        logger.error(f"Aucun fichier CSV trouvé dans {source_dir}")
        return
    elif len(csv_files) > 1:
        logger.warning(f"Plusieurs CSV trouvés, traitement du premier : {csv_files[0]}")

    raw_path = Path(csv_files[0])
    processed_path = PROCESSED_DIR / raw_path.name

    # --- DETECTION DU SEPARATEUR ---
    with open(raw_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        # Si un ";" est présent dans l'entête, on utilise ";", sinon ","
        detected_sep = ';' if ';' in first_line else ','
    
    logger.info(f"Séparateur détecté : '{detected_sep}' pour le fichier {raw_path}")
    logger.info(f"Lecture du fichier {raw_path}")

    df = pd.read_csv(raw_path, sep=detected_sep) 

    logger.info("Début de la normalisation des données")
    try:
        df[["lat", "lon"]] = df["geo_point_2d"].str.split(",", expand=True).astype(float)

        date_col = "Date et heure de comptage"
        df["dt_temp"] = pd.to_datetime(df[date_col], utc=True, errors="coerce")
        df = df.dropna(subset=["dt_temp"])

        df["heure"] = df["dt_temp"].dt.hour
        df["jour_semaine"] = df["dt_temp"].dt.dayofweek
        df["is_weekend"] = (df["jour_semaine"] >= 5).astype(int)

        cols_finales = [
            "Identifiant arc",
            "Date et heure de comptage",
            "Débit horaire",
            "Taux d'occupation",
            "Etat trafic",
            "Identifiant noeud amont",
            "Identifiant noeud aval",
            "Etat arc",
            "geo_point_2d",
            "heure",
            "jour_semaine",
            "is_weekend",
            "lat",
            "lon",
        ]

        missing = [c for c in cols_finales if c not in df.columns]
        if missing:
            raise KeyError(f"Colonnes manquantes: {missing}")

        df = df[cols_finales]

        for col in df.select_dtypes(include="object"):
            df[col] = df[col].astype(str).str.strip()

        logger.info(f"Transformation terminée, {len(df)} lignes traitées")

        # Bonus: mini audit pour voir ce qui change vraiment
        logger.info(f"Etat arc distribution:\n{df['Etat arc'].value_counts(dropna=False).to_string()}")

    except Exception as e:
        logger.exception(f"Erreur lors de la transformation : {e}")
        return

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    stable_out = PROCESSED_DIR / "dataset_processed_current.csv"
    df.to_csv(stable_out, index=False, sep=',') 
    logger.info(f"Dataset stable sauvegardé: {stable_out}")

    # --- archive (optionnel mais recommandé) ---
    history_dir = PROCESSED_DIR / "history"
    history_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_out = history_dir / f"dataset_processed_{stamp}.csv"
    shutil.copyfile(stable_out, archive_out)
    logger.info(f"Archive sauvegardée: {archive_out}")

    # df.to_csv(processed_path, index=False, sep = ',')  # virgule standard
    # logger.info(f"Fichier transformé sauvegardé dans {processed_path}")

if __name__ == "__main__":
    etl_process()