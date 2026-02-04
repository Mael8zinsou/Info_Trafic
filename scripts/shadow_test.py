import json
import os
import sys
import time
import requests

BASE_URL = os.environ.get("BASE_URL", "http://serving:8000")

PAYLOAD = {
  "Identifiant arc": 12345,
  "heure": 8,
  "jour_semaine": 1,
  "is_weekend": 0,
  "Taux d'occupation": 0.80,
  "lat": 48.85,
  "lon": 2.35,
  "Etat arc": "invalide"
}

API_KEY = os.environ.get("SERVING_API_KEY", "")


def wait_health(timeout_s=60):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        try:
            r = requests.get(f"{BASE_URL}/health", timeout=2)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(2)
    return False

# def post(path):
#     r = requests.post(f"{BASE_URL}{path}", json=PAYLOAD, timeout=10)
#     r.raise_for_status()
#     return r.json()

def post(path):
    headers = {"x-api-key": API_KEY} # <--- Ajoute le header ici
    r = requests.post(f"{BASE_URL}{path}", json=PAYLOAD, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()

def main():
    if not wait_health():
        print("[FAIL] API not healthy")
        sys.exit(1)

    p_active = post("/predict")
    p_v2 = post("/predict_v2")

    print("[OK] /predict     :", json.dumps(p_active, ensure_ascii=False))
    print("[OK] /predict_v2  :", json.dumps(p_v2, ensure_ascii=False))

    if p_v2.get("version") != "v2":
        print("[FAIL] /predict_v2 did not return version=v2")
        sys.exit(2)

    print("[OK] Shadow test completed")
    sys.exit(0)

if __name__ == "__main__":
    main()
