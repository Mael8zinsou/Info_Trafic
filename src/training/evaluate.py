# src/training/evaluate.py
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data" / "processed"
MODEL_DIR = ROOT_DIR / "models"

# Doit matcher ton train.py
NUM_FEATURES = [
    "Identifiant arc",
    "heure",
    "jour_semaine",
    "is_weekend",
    "Taux d'occupation",
    "lat",
    "lon",
]
CAT_FEATURES = ["Etat arc"]
TARGET = "Etat trafic"


@dataclass
class EvalResult:
    model_path: str
    dataset_path: str
    n_rows: int
    accuracy: float
    f1_macro: float
    report: str


def evaluate_model(model_path: Path, dataset_path: Path) -> EvalResult:
    df = pd.read_csv(dataset_path)

    # même logique : retirer Inconnu
    df = df[df[TARGET] != "Inconnu"]

    # Si Etat arc absent -> on le crée
    if "Etat arc" not in df.columns:
        df["Etat arc"] = "unknown"
    
    features = NUM_FEATURES + CAT_FEATURES
    df = df.dropna(subset=features + [TARGET])

    X = df[features]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = joblib.load(model_path)

    # --- Alignement des features au modèle entraîné ---
    # Cas 1 : ancien pipeline (v1) entraîné sans Etat arc -> scaler attend seulement NUM_FEATURES
    expected = getattr(model, "feature_names_in_", None)
    if expected is not None:
        # On s’aligne STRICTEMENT sur les colonnes attendues
        X_test = X_test.reindex(columns=list(expected), fill_value="unknown")
    
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    f1m = f1_score(y_test, y_pred, average="macro")

    rep = classification_report(y_test, y_pred)

    return EvalResult(
        model_path=str(model_path),
        dataset_path=str(dataset_path),
        n_rows=len(df),
        accuracy=float(acc),
        f1_macro=float(f1m),
        report=rep,
    )


def as_dict(res: EvalResult) -> Dict[str, Any]:
    return asdict(res)
