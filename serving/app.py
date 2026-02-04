from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from pathlib import Path
import json

from serving.schemas import PredictionInput

# app = FastAPI(title="InfoTrafic – API IA")
app = FastAPI(title="InfoTrafic – API IA (v1 + v2)")


# MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "model_v2.joblib"
# model = None

ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT_DIR / "models"

MODEL_V1_PATH = MODEL_DIR / "model_v1.joblib"
MODEL_V2_PATH = MODEL_DIR / "model_v2.joblib"
ACTIVE_MODEL_PATH = MODEL_DIR / "active_model.json"
REGISTRY_PATH = MODEL_DIR / "registry.json"

models = {"v1": None, "v2": None}



@app.on_event("startup")
def load_models():
    # Charger v1
    if not MODEL_V1_PATH.exists():
        raise RuntimeError(f"Modèle v1 introuvable: {MODEL_V1_PATH}")
    models["v1"] = joblib.load(MODEL_V1_PATH)

    # Charger v2
    if not MODEL_V2_PATH.exists():
        raise RuntimeError(f"Modèle v2 introuvable: {MODEL_V2_PATH}")
    models["v2"] = joblib.load(MODEL_V2_PATH)
# def load_model():
#     global model
#     if not MODEL_PATH.exists():
#         raise RuntimeError(f"Modèle introuvable: {MODEL_PATH}")
#     model = joblib.load(MODEL_PATH)

def get_active_version() -> str:
    # défaut safe
    if not ACTIVE_MODEL_PATH.exists():
        return "v1"

    txt = ACTIVE_MODEL_PATH.read_text(encoding="utf-8").strip()
    if not txt:
        return "v1"

    try:
        data = json.loads(txt)
        v = data.get("active", "v1")
        return v if v in ("v1", "v2") else "v1"
    except json.JSONDecodeError:
        return "v1"

def read_registry():
    if not REGISTRY_PATH.exists():
        return {}
    txt = REGISTRY_PATH.read_text(encoding="utf-8").strip()
    if not txt:
        return {}
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        return {}

def predict_with(model, data: PredictionInput):
    """
    Adapter les features au modèle entraîné:
    - v1: sans 'Etat arc'
    - v2: avec 'Etat arc'
    """
    expected = getattr(model, "feature_names_in_", None)

    # si le modèle expose ses colonnes attendues, on s'aligne dessus
    if expected is not None:
        include_etat_arc = "Etat arc" in list(expected)
        row = data.to_model_dict(include_etat_arc=include_etat_arc)
        X = pd.DataFrame([row])
        # align strict
        X = X.reindex(columns=list(expected), fill_value="unknown")
    else:
        # fallback (rare): on inclut Etat arc
        X = pd.DataFrame([data.to_model_dict(include_etat_arc=True)])

    pred = model.predict(X)
    return str(pred[0])

@app.post("/predict")
def predict(data: PredictionInput):
    version = get_active_version()
    model = models.get(version)

    if model is None:
        raise HTTPException(status_code=500, detail=f"Model {version} not loaded")

    try:
        pred = predict_with(model, data)
        return {"version": version, "prediction": pred}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {e}")
    
@app.post("/predict_v2")
def predict_v2(data: PredictionInput):
    model = models.get("v2")
    if model is None:
        raise HTTPException(status_code=500, detail="Model v2 not loaded")

    try:
        pred = predict_with(model, data)
        return {"version": "v2", "prediction": pred}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {e}")

@app.get("/model/info")
def model_info():
    reg = read_registry()
    return {
        "active": get_active_version(),
        "loaded": {k: (v is not None) for k, v in models.items()},
        "v1_metrics": {k: reg.get("v1", {}).get(k) for k in ("accuracy", "f1_macro", "n_rows")},
        "v2_metrics": {k: reg.get("v2", {}).get(k) for k in ("accuracy", "f1_macro", "n_rows")},
    }

# @app.post("/predict")
# def predict(data: PredictionInput):
#     if model is None:
#         raise HTTPException(status_code=500, detail="Model not loaded")

#     X = pd.DataFrame([data.to_model_dict()])  # 1 ligne

#     try:
#         pred = model.predict(X)
#         return {"prediction": str(pred[0])}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Prediction error: {e}")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "active": get_active_version(),
        "model_v1_loaded": models["v1"] is not None,
        "model_v2_loaded": models["v2"] is not None,
    }

# @app.get("/health")
# def health():
#     return {"status": "ok", "model_loaded": model is not None}
