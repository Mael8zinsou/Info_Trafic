import os
import logging

# Configuration du logger
LOG_DIR = "/app/logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "dataset_fetch.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

SAMPLES_DIR = "samples"
RAW_DIR = "raw"


def fetch_dataset(dataset_name="dossier.csv"):
    """
    - PROD    : télécharge le dataset depuis S3 vers raw/
    - PREPROD : vérifie qu'il existe au moins un fichier .csv dans samples/
    """
    env = os.environ.get("ENV", "PREPROD").upper()
    dest_path = os.path.join(RAW_DIR, dataset_name)

    if env == "PROD":
        import boto3

        bucket_name = os.environ.get("DATA_BUCKET", "my-bucket")
        s3 = boto3.client("s3")

        try:
            os.makedirs(RAW_DIR, exist_ok=True)
            s3.download_file(bucket_name, dataset_name, dest_path)
            logging.info(f"[PROD] Dataset téléchargé depuis S3 : {bucket_name}/{dataset_name}")
        except Exception as e:
            logging.error(f"[PROD] Erreur téléchargement S3 : {e}")

    elif env == "PREPROD":
        if not os.path.isdir(SAMPLES_DIR):
            logging.error(f"[PREPROD] Dossier '{SAMPLES_DIR}' introuvable")
            return None

        csv_files = [f for f in os.listdir(SAMPLES_DIR) if f.lower().endswith(".csv")]

        if csv_files:
            logging.info(f"[PREPROD] {len(csv_files)} fichier(s) CSV trouvé(s) dans samples/")
        else:
            logging.warning("[PREPROD] Aucun fichier CSV trouvé dans samples/")

    else:
        logging.warning(f"ENV non reconnu : {env} (attendu : PROD ou PREPROD)")

    return dest_path


if __name__ == "__main__":
    fetch_dataset()
