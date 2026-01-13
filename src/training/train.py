import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data" / "processed"
MODEL_DIR = ROOT_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

FEATURES = [
    "Identifiant arc",
    "heure",
    "jour_semaine",
    "is_weekend",
    "Taux d'occupation",
    "lat",
    "lon",
]

def load_data():
    df = pd.read_csv(DATA_DIR / "dataset_processed.csv")
    df = df[df["Etat trafic"] != "Inconnu"]
    return df

def split_features_target(df):
    df = df.dropna(subset=FEATURES + ["Etat trafic"])
    X = df[FEATURES]
    y = df["Etat trafic"]
    return X, y

def main():
    df = load_data()
    X, y = split_features_target(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline = Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=5000)),
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy : {accuracy:.3f}")
    print("\nClassification report :")
    print(classification_report(y_test, y_pred))

    joblib.dump(pipeline, MODEL_DIR / "model_v2.joblib")
    print("Pipeline sauvegardé (scaler + modèle)")

if __name__ == "__main__":
    main()