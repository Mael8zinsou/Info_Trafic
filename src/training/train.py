
import pandas as pd
import joblib
from pathlib import Path
from sklearn.discriminant_analysis import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

#BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = Path(__file__).resolve().parents[2]   # remonte de src/training/train.py -> src -> racine projet
DATA_DIR = ROOT_DIR / "data" / "processed"
MODEL_DIR = ROOT_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

def load_data():
    df = pd.read_csv(DATA_DIR / "dataset_processed.csv")
    # Supprimer les lignes avec target Inconnu
    df = df[df["Etat trafic"] != "Inconnu"]
    return df

def split_features_target(df):
    features = [
        "Identifiant arc",
        "heure",
        "jour_semaine",
        "is_weekend",
        "Taux d'occupation",
        "lat",
        "lon"
        
    ]

    df = df.dropna(subset=features + ["Etat trafic"])
    X = df[features]
    y = df["Etat trafic"]

    return X, y

def main():
    df = load_data()
    X, y = split_features_target(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )


# Standardisation des features numériques
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Logistic Regression, augmenter max_iter pour convergence
    model = LogisticRegression(max_iter=5000)
    model.fit(X_train, y_train) 


    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy : {accuracy:.3f}")

    print("\nClassification report :")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, MODEL_DIR / "model_v1.joblib")
    print("Modèle sauvegardé")

if __name__ == "__main__":
    main()
