import joblib
import pandas as pd
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "models"

SAMPLE_ROW = {
    "Identifiant arc": 12345,
    "heure": 8,
    "jour_semaine": 1,
    "is_weekend": 0,
    "Taux d'occupation": 0.42,
    "lat": 48.85,
    "lon": 2.35,
    "Etat arc": "ouvert",
}


@pytest.mark.parametrize("version", ["v1", "v2"])
def test_model_loads_and_predicts(version):
    path = MODELS / f"model_{version}.joblib"
    model = joblib.load(path)
    expected = list(getattr(model, "feature_names_in_", []))
    assert expected, f"{version} doit exposer feature_names_in_"

    X = pd.DataFrame([SAMPLE_ROW]).reindex(columns=expected, fill_value="unknown")
    pred = model.predict(X)
    assert len(pred) == 1
    assert isinstance(str(pred[0]), str)


def test_v2_uses_etat_arc_but_v1_does_not():
    """Contrat anti-drift : v1 ignore 'Etat arc', v2 l'utilise."""
    v1 = joblib.load(MODELS / "model_v1.joblib")
    v2 = joblib.load(MODELS / "model_v2.joblib")
    assert "Etat arc" not in list(v1.feature_names_in_)
    assert "Etat arc" in list(v2.feature_names_in_)
