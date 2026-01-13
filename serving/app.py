from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from pathlib import Path

from serving.schemas import PredictionInput

app = FastAPI(title="InfoTrafic – API IA")

# ROOT_DIR = Path(__file__).resolve().parents[2]   # remonte de src/training/train.py -> src -> racine projet
# DATA_DIR = ROOT_DIR / "data" / "processed"
# MODEL_DIR = ROOT_DIR / "models"
# MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "model_v1.joblib"

model = None


@app.on_event("startup")
def load_model():
    global model
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Modèle introuvable: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)


@app.post("/predict")
def predict(data: PredictionInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # Convertit le dict en note: 1 ligne = 1 observation
    X = pd.DataFrame([data.features])

    try:
        pred = model.predict(X)
        return {"prediction": str(pred[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {e}")


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}
