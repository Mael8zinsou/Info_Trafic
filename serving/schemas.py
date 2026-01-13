from pydantic import BaseModel, Field

class PredictionInput(BaseModel):
    identifiant_arc: float = Field(..., alias="Identifiant arc")
    heure: float
    jour_semaine: float
    is_weekend: float
    taux_occupation: float = Field(..., alias="Taux d'occupation")
    lat: float
    lon: float

    def to_model_dict(self):
        # Re-crée EXACTEMENT les noms attendus par le modèle
        return {
            "Identifiant arc": self.identifiant_arc,
            "heure": self.heure,
            "jour_semaine": self.jour_semaine,
            "is_weekend": self.is_weekend,
            "Taux d'occupation": self.taux_occupation,
            "lat": self.lat,
            "lon": self.lon,
        }
