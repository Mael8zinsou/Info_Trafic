# 📊 Monitoring — Prometheus + Grafana

Stack d'observabilité pour le serving InfoTrafic. Toute l'infra est conteneurisée et provisionnée automatiquement par Docker Compose : `docker compose up` suffit.

---

## 🚀 Lancement

```bash
# Démarre serving + Prometheus + Grafana
docker compose -p infotraf up -d --build serving prometheus grafana

# Génère un peu de trafic pour voir les graphes vivre
python scripts/load_test.py --duration 120 --rps 5
```

| Service | URL | Notes |
| --- | --- | --- |
| Serving FastAPI | http://localhost:8001 | API ML + `/metrics` Prometheus |
| Swagger UI | http://localhost:8001/docs | Doc auto-générée de l'API |
| Prometheus | http://localhost:9090 | Targets : http://localhost:9090/targets |
| Grafana | http://localhost:3000 | admin / admin (ou anonyme en Viewer) |
| Dashboard | http://localhost:3000/d/infotrafic-serving | Vue principale ML serving |

---

## 📐 Architecture

```
┌──────────────────┐    scrape /metrics   ┌──────────────┐    query    ┌─────────────┐
│ serving (FastAPI)│ ◀───── 5s ───────── │  Prometheus  │ ◀────────── │   Grafana   │
│  :8000  /metrics │                      │   :9090      │             │   :3000     │
└──────────────────┘                      └──────────────┘             └─────────────┘
        ▲                                       │                            │
        │ POST /predict                         │                            │ provisioning
        │ POST /predict_v2                      │ TSDB (7j retention)        │ auto :
        │                                       │ volume: prometheus_data    │ - datasource
   ┌────┴─────┐                                 │                            │ - dashboard
   │ load_test│                                 │                            ▼
   │  .py     │                                 │                      [Dashboard JSON]
   └──────────┘                                                         monitoring/grafana/
                                                                        dashboards/*.json
```

---

## 📈 Métriques exposées

### Standard HTTP (via `prometheus-fastapi-instrumentator`)

Auto-collectées sur chaque requête, accessibles sur `GET /metrics` :

- `http_requests_total{handler, method, status}` — Counter
- `http_request_duration_seconds_bucket{handler, method}` — Histogram
- `http_requests_inprogress{handler, method}` — Gauge

### Custom ML (déclarées dans `serving/app.py`)

| Métrique | Type | Labels | Sens |
| --- | --- | --- | --- |
| `ml_predictions_total` | Counter | `version`, `prediction_class` | Volume de prédictions, ventilé par modèle et par classe prédite (Fluide / Pré-saturé / Saturé / Bloqué) |
| `ml_prediction_latency_seconds` | Histogram | `version` | Temps d'inférence pur (hors HTTP), buckets 1ms → 2.5s |
| `ml_active_model` | Gauge | `version` | 1 si actif, 0 sinon — reflète `models/active_model.json` |
| `ml_shadow_disagreements_total` | Counter | — | Incrémenté quand `/predict_v2` produit une prédiction différente de la version active (anti-drift) |

---

## 🎨 Dashboard Grafana

Le dashboard `InfoTrafic — ML Serving` est provisionné automatiquement avec 7 panels :

1. **Active model** (stat) — version actuellement servie via `/predict`
2. **Total predictions** (stat) — volume sur les 5 dernières minutes
3. **Shadow disagreements** (stat) — désaccords v1 vs v2 récents (seuils 5/20)
4. **Error rate** (stat) — ratio 4xx+5xx, seuils 1% / 5%
5. **Request rate** (timeseries) — req/s par endpoint
6. **Prediction latency** (timeseries) — p50/p95/p99 par version
7. **Predictions per class** (timeseries empilé) — répartition par version × classe

Refresh auto : 5s. Time range : last 15 min.

---

## 🔧 Provisioning détaillé

### Prometheus

Config : [monitoring/prometheus/prometheus.yml](../monitoring/prometheus/prometheus.yml)

- `scrape_interval: 5s` (intervalle court pour avoir un dashboard réactif en démo)
- Jobs :
  - `serving` → `serving:8000/metrics` (résolution DNS via le réseau Docker `ml-network`)
  - `prometheus` → lui-même (self-monitoring)
- Stockage TSDB local, rétention 7 jours, volume nommé `prometheus_data`

### Grafana

Provisioning via fichiers, [monitoring/grafana/provisioning/](../monitoring/grafana/provisioning/) :

```
provisioning/
├── datasources/prometheus.yml    # datasource Prometheus par défaut
└── dashboards/dashboards.yml     # provider qui scanne /var/lib/grafana/dashboards
```

Dashboards montés en read-only depuis [monitoring/grafana/dashboards/](../monitoring/grafana/dashboards/). Pour ajouter un dashboard : drop un JSON dans ce dossier, Grafana le détecte en 30s (`updateIntervalSeconds: 30`).

Accès :
- Anonyme en Viewer (lecture seule) — parfait pour une démo / capture d'écran
- `admin / admin` pour modifier les dashboards via l'UI

---

## 🎯 Générer du trafic pour la démo

```bash
# Trafic nominal — peu de désaccords v1/v2
python scripts/load_test.py --duration 300 --rps 5 --degraded-ratio 0.1

# Conditions dégradées — force la divergence v1/v2 (panel "Shadow disagreements")
python scripts/load_test.py --duration 180 --rps 8 --degraded-ratio 0.6 --shadow-ratio 0.5
```

Flags :

| Flag | Effet |
| --- | --- |
| `--duration` | Durée en secondes (défaut 120) |
| `--rps` | Cible de requêtes/s (défaut 3) |
| `--degraded-ratio` | Proportion de payloads "capteur invalide / occupation haute" |
| `--shadow-ratio` | Proportion envoyée sur `/predict_v2` au lieu de `/predict` |

Le payload "dégradé" force `Etat arc=invalide` + `Taux d'occupation > 0.6` — c'est exactement le scénario où v1 (qui ignore `Etat arc`) reste optimiste et v2 (qui s'en méfie) bascule sur "Pré-saturé". Le compteur `ml_shadow_disagreements_total` s'incrémente alors visiblement.

---

## 🧹 Cleanup

```bash
docker compose -p infotraf down
# pour aussi supprimer les volumes (perd l'historique TSDB Prometheus) :
docker compose -p infotraf down -v
```
