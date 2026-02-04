from pydantic import BaseModel, Field

# from pydantic import BaseModel, Field, conint, confloat
# class PredictionInput(BaseModel):
#     identifiant_arc: confloat(gt=0)
#     heure: conint(ge=0, le=23)
#     jour_semaine: conint(ge=0, le=6)
#     is_weekend: conint(ge=0, le=1)
#     taux_occupation: confloat(ge=0.0)
#     lat: confloat(ge=-90.0, le=90.0)
#     lon: confloat(ge=-180.0, le=180.0)
#     etat_arc: str = "unknown"

class PredictionInput(BaseModel):
    identifiant_arc: float = Field(..., alias="Identifiant arc")
    heure: float
    jour_semaine: float
    is_weekend: float
    taux_occupation: float = Field(..., alias="Taux d'occupation")
    lat: float
    lon: float
    etat_arc: str = Field("unknown", alias="Etat arc")  # NEW (v2)

    def to_model_dict(self, include_etat_arc: bool = True):
        # Re-crée EXACTEMENT les noms attendus par le modèle
        row = {
            "Identifiant arc": self.identifiant_arc,
            "heure": self.heure,
            "jour_semaine": self.jour_semaine,
            "is_weekend": self.is_weekend,
            "Taux d'occupation": self.taux_occupation,
            "lat": self.lat,
            "lon": self.lon,
        }
        # v2 attend Etat arc, v1 non. On choisit selon le modèle.
        if include_etat_arc:
            row["Etat arc"] = self.etat_arc
        return row

