import os
import pytest
from fastapi.testclient import TestClient


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
    # On force la clé AVANT le premier import du module (sinon API_KEY=""
    # est figée au top-level de serving.app et l'app tourne en mode public).
    monkeypatch_module.setenv("SERVING_API_KEY", "test-key-pytest")
    import serving.app as serving_app
    # Patch direct de la variable module — load_dotenv a pu écraser l'env var
    # depuis un .env voisin lors du premier import.
    serving_app.API_KEY = "test-key-pytest"
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
