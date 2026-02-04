import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.utils.log_utils import get_logger


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data" / "processed"
MODEL_DIR = ROOT_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

LOG_DIR = ROOT_DIR / "logs"
logger = get_logger("training", LOG_DIR / "training.log")

# --- Features ---
NUM_FEATURES = [
    "Identifiant arc",
    "heure",
    "jour_semaine",
    "is_weekend",
    "Taux d'occupation",
    "lat",
    "lon",
]

CAT_FEATURES = [
    "Etat arc",  # nouvelle réalité : qualité capteur
]

def load_data(dataset_filename="dataset_processed_current.csv"):
    path = DATA_DIR / dataset_filename
    logger.info(f"Chargement dataset: {path}")
    df = pd.read_csv(DATA_DIR / dataset_filename)
    logger.info(f"Dataset chargé: {len(df)} lignes, {len(df.columns)} colonnes")


    # On garde la même logique : enlever Inconnu
    if "Etat trafic" not in df.columns:
        raise KeyError("Colonne 'Etat trafic' introuvable dans le dataset.")
    df = df[df["Etat trafic"] != "Inconnu"]
    logger.info(f"Après filtre TARGET != Inconnu: {len(df)} lignes")

    return df

# dataset_path = DATA_DIR / "traffic_normalized.csv"
# def load_data(dataset_path: Path) -> pd.DataFrame:
#     df = pd.read_csv(dataset_path)

#     # On garde la même logique : enlever Inconnu
#     if "Etat trafic" not in df.columns:
#         raise KeyError("Colonne 'Etat trafic' introuvable dans le dataset.")
#     df = df[df["Etat trafic"] != "Inconnu"]

#     return df


def split_features_target(df: pd.DataFrame):
    # Drop NA sur features + target (logique identique)
    features = NUM_FEATURES + CAT_FEATURES
    df = df.dropna(subset= features + ["Etat trafic"])

    X = df[features]
    y = df["Etat trafic"]

    logger.info(f"Features num: {NUM_FEATURES}")
    logger.info(f"Features cat: {CAT_FEATURES}")
    logger.info(f"Distribution target:\n{y.value_counts(dropna=False).to_string()}")
    return X, y


def training_process_2(dataset_filename: str = "dataset_processed_current.csv", model_name: str = "model_v2.joblib"):
    dataset_path = DATA_DIR / dataset_filename

    try:
        df = load_data(dataset_path)
        X, y = split_features_target(df)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.2,
            random_state=42,
            stratify=y  # léger mieux si classes déséquilibrées
        )

        # Preprocessing minimal mais correct : scaler sur numériques, onehot sur Etat arc
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), NUM_FEATURES),
                ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_FEATURES),
            ]
        )

        pipeline = Pipeline(steps=[
            ("preprocess", preprocessor),
            ("clf", LogisticRegression(max_iter=5000, class_weight="balanced")),
        ])

        logger.info("Début fit du pipeline...")
        pipeline.fit(X_train, y_train)
        logger.info("Fit terminé.")

        y_pred = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1m = f1_score(y_test, y_pred, average="macro")

        logger.info(f"Metrics: accuracy={accuracy:.4f} | f1_macro={f1m:.4f}")
        rep = classification_report(y_test, y_pred)
        logger.info(f"Classification report:\n{rep}")

        print(f"Dataset: {dataset_path}")
        print(f"Accuracy : {accuracy:.3f}")
        print("\nClassification report :")
        print(classification_report(y_test, y_pred))

        out_path = MODEL_DIR / model_name
        joblib.dump(pipeline, out_path)
        logger.info(f"Modèle sauvegardé: {out_path}")
        print("Pipeline sauvegardé (scaler + modèle)")

        # Bonus: sauver le report dans un fichier
        report_path = MODEL_DIR / f"report_{model_name.replace('.joblib','')}.txt"
        report_path.write_text(rep, encoding="utf-8")
        logger.info(f"Report sauvegardé: {report_path}")
    except Exception as e:
        logger.exception(f"Erreur durant le training: {e}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="dataset_processed_current.csv")
    parser.add_argument("--model", type=str, default="model_v2.joblib")
    args = parser.parse_args()

    training_process_2(dataset_filename=args.dataset, model_name=args.model)