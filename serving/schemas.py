from pydantic import BaseModel, Field
from typing import Dict

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


class PredictionInput(BaseModel):
    features: Dict[str, float] = Field(
        # "Identifiant arc",
        # "heure",
        # "jour_semaine",
        # "is_weekend",
        # "Taux d'occupation",
        # "lat",
        # "lon",
        description="Dictionnaire {nom_feature: valeur} correspondant aux features du modèle"
    )

'''class PredictionInput(BaseModel):
    features: Dict[str, float] = Field(
        ...,
        description="Dictionnaire {nom_feature: valeur} correspondant aux features du modèle"
    )'''
