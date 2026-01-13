import os
import glob
import pandas as pd
import logging

# Config logs
LOG_DIR = "/app/logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "etl.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

PROCESSED_DIR = "/app/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

def etl_process():
    env = os.environ.get("ENV", "preprod").lower()
    if env == "prod":
        source_dir = "/app/raw"
    elif env == "preprod":
        source_dir = "/app/samples"
    else:
        logging.warning(f"ENV non reconnu ({env}), utilisation de preprod par défaut")
        source_dir = "/app/samples"

    # Cherche le seul CSV dans le dossier source
    csv_files = glob.glob(os.path.join(source_dir, "*.csv"))
    if not csv_files:
        logging.error(f"Aucun fichier CSV trouvé dans {source_dir}")
        return
    elif len(csv_files) > 1:
        logging.warning(f"Plusieurs CSV trouvés dans {source_dir}, traitement du premier : {csv_files[0]}")

    raw_path = csv_files[0]
    filename = os.path.basename(raw_path)
    processed_path = os.path.join(PROCESSED_DIR, filename)

    # Extract
    logging.info(f"Lecture du fichier {raw_path}")
    df = pd.read_csv(raw_path, sep=";")  # adapte le séparateur si nécessaire

    # Transform (exemple simple)
    df.dropna(inplace=True)  # supprimer lignes vides
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.strip()  # nettoyer espaces
    logging.info(f"Transformation terminée, {len(df)} lignes conservées")

    # Load
    df.to_csv(processed_path, index=False, sep=";")
    logging.info(f"Fichier transformé sauvegardé dans {processed_path}")

if __name__ == "__main__":
    etl_process()