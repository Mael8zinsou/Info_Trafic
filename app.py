# app.py

import argparse
import time
import threading
import logging
from pathlib import Path
from src.etl.app import etl_process
from src.training.train_v2 import training_process_2

# =========================
# CONFIGURATION LOGS
# =========================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "api.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("api")

# =========================
# JOBS
# =========================

def ingest():
    logger.info("📥 Lancement de l’ingestion")
    time.sleep(2)
    logger.info("✅ Ingestion terminée")

def etl():
    logger.info("🔄 Lancement de l’ETL")
    etl_process()
    logger.info("✅ ETL terminé")

def training():
    logger.info("🤖 Lancement du training ML")
    logger.info("Dataset: data/processed/dataset_processed_current.csv")

    try:
        training_process_2(
            dataset_filename="dataset_processed_current.csv",
            model_name="model_v2.joblib"
        )
        logger.info("✅ Training terminé")
    except Exception:
        logger.exception("❌ Erreur durant le training")

# =========================
# API
# =========================

def run_api():
    from fastapi import FastAPI
    from pydantic import BaseModel
    import uvicorn

    app = FastAPI(
        title="API Info Trafic",
        description="API pour ingestion, ETL et training",
        version="1.0"
    )

    class JobRequest(BaseModel):
        mode: str

    @app.get("/status", tags=["Info"])
    def status():
        logger.info("Status check")
        return {"status": "API OK"}

    @app.post("/run-job", tags=["Jobs"])
    def run_job(request: JobRequest):
        mode = request.mode.lower()
        logger.info(f"Requête job reçue : {mode}")

        def target():
            try:
                if mode == "ingest":
                    ingest()
                elif mode == "etl":
                    etl()
                elif mode == "training":
                    training()
                else:
                    logger.error(f"Mode inconnu : {mode}")
            except Exception:
                logger.exception(f"Erreur job {mode}")

        threading.Thread(target=target, daemon=True).start()
        return {"status": f"{mode} lancé en arrière-plan"}

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

# =========================
# ENTRYPOINT
# =========================

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["ingest", "etl", "training", "api"],
        required=True
    )
    args = parser.parse_args()

    logger.info(f"Lancement en mode : {args.mode}")

    if args.mode == "ingest":
        ingest()
    elif args.mode == "etl":
        etl()
    elif args.mode == "training":
        training()
    elif args.mode == "api":
        run_api()