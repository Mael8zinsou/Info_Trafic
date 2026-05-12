# src/training/compare_models.py
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

import pandas as pd

#from src.training.evaluate import evaluate_model, as_dict, NUM_FEATURES, CAT_FEATURES
from src.training.evaluate import evaluate_model, as_dict, NUM_FEATURES, CAT_FEATURES

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data" / "processed"
MODEL_DIR = ROOT_DIR / "models"

REGISTRY_PATH = MODEL_DIR / "registry.json"
COMPARE_OUT = MODEL_DIR / "comparison_v1_v2.csv"

model_v1 = 'model_v1.joblib'
model_v2 = 'model_v2.joblib'
dataset = 'traffic_normalized.csv'

def load_registry() -> Dict[str, Any]:
    if not REGISTRY_PATH.exists():
        return {}
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def save_registry(reg: Dict[str, Any]) -> None:
    REGISTRY_PATH.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")


def main(model_v1: str, model_v2: str, dataset: str, out_csv: str):
    model_v1_path = MODEL_DIR / model_v1
    model_v2_path = MODEL_DIR / model_v2
    dataset_path = DATA_DIR / dataset

    if not model_v1_path.exists():
        raise FileNotFoundError(f"Modèle introuvable: {model_v1_path}")
    if not model_v2_path.exists():
        raise FileNotFoundError(f"Modèle introuvable: {model_v2_path}")
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset introuvable: {dataset_path}")

    res1 = evaluate_model(model_v1_path, dataset_path)
    res2 = evaluate_model(model_v2_path, dataset_path)

    df = pd.DataFrame([
        {"version": "v1", "accuracy": res1.accuracy, "f1_macro": res1.f1_macro, "n_rows": res1.n_rows},
        {"version": "v2", "accuracy": res2.accuracy, "f1_macro": res2.f1_macro, "n_rows": res2.n_rows},
    ])

    out_path = MODEL_DIR / out_csv
    df.to_csv(out_path, index=False)
    print(f"[OK] Tableau comparatif écrit: {out_path}\n")
    print(df)

    # registry minimal
    reg = load_registry()
    now = datetime.now().isoformat(timespec="seconds")

    rel_v1 = model_v1_path.relative_to(ROOT_DIR).as_posix()
    rel_v2 = model_v2_path.relative_to(ROOT_DIR).as_posix()
    rel_dataset = dataset_path.relative_to(ROOT_DIR).as_posix()

    reg["v1"] = {
        "timestamp": now,
        "model_path": rel_v1,
        "dataset_eval": rel_dataset,
        "features_num": NUM_FEATURES,
        "features_cat": CAT_FEATURES,
        **as_dict(res1),
    }
    reg["v2"] = {
        "timestamp": now,
        "model_path": rel_v2,
        "dataset_eval": rel_dataset,
        "features_num": NUM_FEATURES,
        "features_cat": CAT_FEATURES,
        **as_dict(res2),
    }

    save_registry(reg)
    print(f"[OK] Registry mis à jour: {REGISTRY_PATH}")

    # Optionnel: dump reports dans des txt (plus lisible)
    (MODEL_DIR / "report_v1.txt").write_text(res1.report, encoding="utf-8")
    (MODEL_DIR / "report_v2.txt").write_text(res2.report, encoding="utf-8")
    print("[OK] Reports écrits: models/report_v1.txt, models/report_v2.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_v1", type=str, default="model_v1.joblib")
    parser.add_argument("--model_v2", type=str, default="model_v2.joblib")
    parser.add_argument("--dataset", type=str, default="traffic_normalized.csv")
    parser.add_argument("--out", type=str, default="comparison_v1_v2.csv")
    args = parser.parse_args()

    main(args.model_v1, args.model_v2, args.dataset, args.out)
