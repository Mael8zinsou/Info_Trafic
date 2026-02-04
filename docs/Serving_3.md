# TP3 — Serving v1/v2 + bascule contrôlée

## Objectif
- Exposer v1 et v2 sans rupture de service
- Permettre un mode shadow (v2 en parallèle)
- Préparer une bascule réversible (rollback)

## Endpoints
- GET /health : état du service + version active
- POST /predict : utilise la version active (v1 ou v2)
- POST /predict_v2 : force v2 (shadow testing)
- GET /model/info : métriques v1/v2 depuis models/registry.json

## Pilotage de la version active
Fichier : models/active_model.json
- {"active":"v1"} => production sur v1
- {"active":"v2"} => production sur v2

Rollback : remettre "v1".

## Lancer en local
uvicorn serving.app:app --host 0.0.0.0 --port 8000

## Lancer avec Docker
docker compose up -d serving

## Shadow test automatisé
docker compose run --rm tester

Le tester compare /predict et /predict_v2 sur un payload de test
et vérifie que v2 répond correctement.
