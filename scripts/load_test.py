"""
Générateur de trafic synthétique pour la démo monitoring.

Usage local (stack docker-compose up) :
    python scripts/load_test.py
    python scripts/load_test.py --duration 300 --rps 5 --shadow-ratio 0.3

Le script alterne entre payloads "normaux" (trafic fluide) et payloads
"dégradés" (Etat arc invalide, taux d'occupation élevé) pour faire diverger
v1 et v2 — visible sur le panel "Shadow disagreements" du dashboard Grafana.
"""
import argparse
import os
import random
import time
from typing import Dict, Any

import requests


BASE_URL = os.environ.get("BASE_URL", "http://localhost:8001")
API_KEY = os.environ.get("SERVING_API_KEY", "mon_secret_ultra_securise_2026")

ETAT_ARC_NORMAL = ["ouvert", "ouvert", "ouvert", "barre"]
ETAT_ARC_DEGRADED = ["invalide", "invalide", "barre", "ouvert"]

ARC_IDS = [5462, 5468, 5470, 5475, 5489, 5512, 5525, 5560]


def make_payload(degraded: bool = False) -> Dict[str, Any]:
    is_weekend = random.choice([0, 0, 0, 0, 0, 1, 1])
    heure = random.randint(0, 23)
    occ = random.uniform(0.6, 0.95) if degraded else random.uniform(0.05, 0.7)
    etat = random.choice(ETAT_ARC_DEGRADED if degraded else ETAT_ARC_NORMAL)
    return {
        "Identifiant arc": random.choice(ARC_IDS),
        "heure": heure,
        "jour_semaine": random.randint(0, 6),
        "is_weekend": is_weekend,
        "Taux d'occupation": round(occ, 3),
        "lat": round(random.uniform(48.82, 48.89), 5),
        "lon": round(random.uniform(2.27, 2.40), 5),
        "Etat arc": etat,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=120, help="Durée en secondes (def 120)")
    parser.add_argument("--rps", type=float, default=3.0, help="Requêtes par seconde (def 3)")
    parser.add_argument("--degraded-ratio", type=float, default=0.3,
                        help="Proportion de payloads dégradés (def 0.3) — fait diverger v1/v2")
    parser.add_argument("--shadow-ratio", type=float, default=0.4,
                        help="Proportion de requêtes envoyées sur /predict_v2 (def 0.4)")
    args = parser.parse_args()

    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
    delay = 1.0 / args.rps
    deadline = time.time() + args.duration
    sent = 0
    errors = 0

    print(f"-> Cible : {BASE_URL}")
    print(f"-> Durée : {args.duration}s @ {args.rps} req/s (~{int(args.duration * args.rps)} req)")
    print(f"-> Dégradés : {int(args.degraded_ratio * 100)}%  |  Shadow (/predict_v2) : {int(args.shadow_ratio * 100)}%")
    print()

    try:
        while time.time() < deadline:
            degraded = random.random() < args.degraded_ratio
            payload = make_payload(degraded=degraded)
            path = "/predict_v2" if random.random() < args.shadow_ratio else "/predict"
            try:
                r = requests.post(f"{BASE_URL}{path}", json=payload, headers=headers, timeout=5)
                if r.status_code != 200:
                    errors += 1
            except requests.RequestException:
                errors += 1
            sent += 1
            if sent % 20 == 0:
                print(f"  [{sent} req | {errors} errors]")
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\n[interrupted]")

    print(f"\n[done] {sent} req sent, {errors} errors")
    print(f"-> Voir le dashboard : http://localhost:3000/d/infotrafic-serving")


if __name__ == "__main__":
    main()
