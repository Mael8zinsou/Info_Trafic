# app.py

import argparse
import logging
import threading

from src.ingest.app import ingest_run
from src.etl.app import etl_process
from src.training.train import main

# Configuration simple, une fois
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),  # fichier dans ton dossier logs
        logging.StreamHandler()               # affichage console
    ]
)

def ingest():
    logger = logging.getLogger("ingest")
    logger.info("📥 Lancement de l’ingestion...")
    ingest_run()
    logger.info("✅ Ingestion terminée !")

def etl():
    logger = logging.getLogger("etl")
    logger.info("🔄 Lancement de l’ETL...")
    etl_process()
    logger.info("✅ ETL terminé !")
def training():
    logger = logging.getLogger("training")
    logger.info("🤖 Lancement du training ML...")
    main()
    logger.info("✅ Training terminé !")
def run_api():

    from fastapi import FastAPI

    from pydantic import BaseModel

    import uvicorn

    app = FastAPI(

        title="API Info Trafic",

        description="API pour gérer ingestion, ETL et training",

        version="1.0"

    )

    class JobRequest(BaseModel):

        mode: str

    @app.get("/status", tags=["Info"])

    def status():

        return {"status": "API OK"}
    @app.post("/run-job", tags=["Jobs"])

    def run_job(request: JobRequest):

        mode = request.mode.lower()

        def target():

            if mode == "ingest":

                ingest()

            elif mode == "etl":

                etl()

            elif mode == "training":

                training()

            else:

                print(f"❌ Mode inconnu : {mode}")

        threading.Thread(target=target).start()

        return {"status": f"{mode} lancé en arrière-plan"}

    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--mode", choices=["ingest", "etl", "training", "api"], required=True)

    args = parser.parse_args()

    if args.mode == "ingest":

        ingest()

    elif args.mode == "etl":

        etl()

    elif args.mode == "training":

        training()

    elif args.mode == "api":

        run_api()