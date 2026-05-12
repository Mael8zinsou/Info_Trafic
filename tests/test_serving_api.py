import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "models"
MODELS_AVAILABLE = (MODELS / "model_v1.joblib").exists() and (MODELS / "model_v2.joblib").exists()
pytestmark = pytest.mark.skipif(
    not MODELS_AVAILABLE,
    reason="Modèles .joblib absents (gitignored) — tests serving skip en CI sans artefact",
)


PAYLOAD = {
    "Identifiant arc": 12345,
    "heure": 8,
    "jour_semaine": 1,
    "is_weekend": 0,
    "Taux d'occupation": 0.42,
    "lat": 48.85,
    "lon": 2.35,
    "Etat arc": "ouvert",
}


@pytest.fixture(scope="module")
def app_module(monkeypatch_module):
    monkeypatch_module.setenv("SERVING_API_KEY", "test-key-pytest")
    from importlib import reload
    import serving.app as serving_app
    reload(serving_app)
    return serving_app


@pytest.fixture(scope="module")
def monkeypatch_module():
    from _pytest.monkeypatch import MonkeyPatch
    mp = MonkeyPatch()
    yield mp
    mp.undo()


@pytest.fixture(scope="module")
def client(app_module):
    with TestClient(app_module.app) as c:
        yield c


def test_health_endpoint_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["active"] in ("v1", "v2")
    assert body["model_v1_loaded"] is True
    assert body["model_v2_loaded"] is True


def test_predict_rejects_missing_api_key(client):
    r = client.post("/predict", json=PAYLOAD)
    assert r.status_code == 401


def test_predict_accepts_valid_api_key(client):
    r = client.post("/predict", json=PAYLOAD, headers={"x-api-key": "test-key-pytest"})
    assert r.status_code == 200
    body = r.json()
    assert body["version"] in ("v1", "v2")
    assert isinstance(body["prediction"], str)
