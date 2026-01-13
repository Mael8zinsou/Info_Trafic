import os
import shutil
import logging

# Configuration du logger
LOG_DIR = "/app/logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "dataset_fetch.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_dataset(dataset_name="dossier.csv"):
    """
    Récupère le dataset selon l'environnement :
    - En prod : le chercher sur AWS S3
    - En preprod : vérifier sa présence dans data/, le déplacer/copier dans raw/
    """
    env = os.environ.get("ENV", "preprod").lower()
    dest_path = os.path.join("raw", dataset_name)

    if env == "prod":
        import boto3
        s3 = boto3.client("s3")
        bucket_name = os.environ.get("DATA_BUCKET", "my-bucket")
        try:
            s3.download_file(bucket_name, dataset_name, dest_path)
            logging.info(f"Dataset récupéré depuis S3 : {bucket_name}/{dataset_name}")
        except Exception as e:
            logging.error(f"Erreur lors du téléchargement depuis S3: {e}")
    elif env == "preprod":
        if os.path.exists(dest_path):
            logging.info(f"Le fichier {dest_path} existe déjà dans raw/")
        else:
            logging.warning(f"Fichier {dest_path} introuvable dans raw/")
    else:
        logging.warning("ENV non reconnu. Valeurs attendues : 'prod' ou 'preprod'.")

    return dest_path

if __name__ == "__main__":
    fetch_dataset()