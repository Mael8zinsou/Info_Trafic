# 📦 Serving IA : v1 / v2, Shadow Testing et Bascule Contrôlée

## 🎯 Objectifs

Cette brique logicielle assure la transition entre l'entraînement et l'utilisation réelle. L'objectif est de fournir un **environnement de production sécurisé** permettant d'itérer sur les modèles sans risque de régression.

* **Multi-versioning :** Coexistence des modèles `v1` (baseline) et `v2` (robuste au drift).
* **Shadow Testing :** Évaluation de la `v2` en conditions réelles sans impact utilisateur.
* **Bascule "Zero-Downtime" :** Passage d'une version à l'autre via configuration dynamique.
* **Sécurisation :** Protection des accès via authentification par clé API.

---

## 🧠 Architecture du Service

Le service repose sur **FastAPI** conteneurisé. Contrairement à un déploiement classique, l'API charge **tous les modèles en mémoire** au démarrage pour permettre un switch instantané.

> [!NOTE]
> **Le cerveau hybride :** L'API ne se contente pas de prédire ; elle arbitre. Elle utilise une "source de vérité" (fichier JSON) pour savoir quel modèle doit répondre à la route de production.

---

## 🔌 Interface de l'API (Endpoints)

| Méthode | Route | Rôle | Sécurité |
| --- | --- | --- | --- |
| `GET` | `/health` | Vérifie l'état de l'API et le chargement des modèles. | Ouverte |
| `POST` | `/predict` | **Production :** Prédiction via le modèle actif. | API Key |
| `POST` | `/predict_v2` | **Shadow :** Force l'utilisation de la V2 pour test. | API Key |
| `GET` | `/model/info` | Expose les métriques (Accuracy, F1) du `registry.json`. | API Key |

---

## 🧭 Pilotage de la Production (Bascule & Rollback)

La gestion du **Blue-Green Deployment** ne se fait pas au niveau de l'infrastructure, mais via un fichier de configuration dynamique situé dans le volume partagé : `models/active_model.json`.

### Scénarios de configuration :

* **Mode Blue (V1) :** `{ "active": "v1" }`
* **Mode Green (V2) :** `{ "active": "v2" }`

**L'avantage majeur :** En cas d'anomalie sur la V2, le **rollback** consiste à modifier une seule ligne du JSON. L'API détecte le changement (au prochain appel ou via rafraîchissement) et redirige le flux vers la V1 immédiatement, sans redémarrage.

---

## 🧪 Validation par Shadow Testing

Avant toute bascule, nous utilisons le script `scripts/shadow_test.py`. Ce mécanisme permet de comparer les performances des deux modèles sur un même flux de données.

**Exécution via Docker :**

```bash
docker compose run --rm tester

```

Le container `tester` compare les réponses de `/predict` et `/predict_v2`. Si les résultats de la V2 sont cohérents sur les cas critiques (ex: arcs invalides), la bascule est autorisée.

---

## 🔐 Sécurisation des accès

L'accès externe est verrouillé par un mécanisme de **Clé API**.

* **Header requis :** `x-api-key: <votre_cle_secrete>`
* **Logique :** La clé est récupérée via les variables d'environnement (`SERVING_API_KEY`). Si la clé fournie est absente ou incorrecte, l'API renvoie une erreur `401 Unauthorized`.

---

## 🚀 Guide de lancement

### Environnement de Développement (Local)

```bash
# Nécessite un fichier .env chargé
uvicorn serving.app:app --host 0.0.0.0 --port 8000

```

### Environnement de Staging/Prod (Docker)

```bash
# Build et lancement en mode détaché
docker compose up -d serving

```
