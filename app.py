# app.py

import argparse

import time

import threading

from src.training.train import main

def ingest():

    print("📥 Lancement de l’ingestion...")

    time.sleep(2)

    print("✅ Ingestion terminée !")

def etl():

    print("🔄 Lancement de l’ETL...")

    time.sleep(3)

    print("✅ ETL terminé !")

def training():

    print("🤖 Lancement du training ML...")
    print("📦 Délégation vers src.training.train")

    main()
    time.sleep(5)

    print("✅ Training terminé !")

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