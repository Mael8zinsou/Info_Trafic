# 🚦 InfoTrafic — Projet Fil Rouge MLOps

**Industrialisation d’un modèle de prédiction de l’état du trafic**

---

## 🎯 Objectif du projet

**InfoTrafic** est un projet fil rouge visant à concevoir une **chaîne MLOps complète**, de la donnée brute jusqu’au serving sécurisé d’un modèle de machine learning.

Le projet met l’accent sur :

* la **robustesse du pipeline**,
* la **gestion de la dérive des données**,
* l’**évolution contrôlée des modèles**,
* la **sécurité, la conformité et la gouvernance de l’IA**.

Il s’inscrit dans un cadre académique, avec une approche réaliste inspirée de contextes industriels.

---

## 🧠 Cas d’usage

À partir de données Open Data issues de capteurs routiers parisiens, le système prédit l’**état du trafic** (ex. Fluide, Pré-saturé, Saturé) pour un segment routier donné, en fonction de :

* l’heure et le jour,
* le taux d’occupation,
* la localisation,
* l’état de validité du capteur.

Le système agit comme **une aide à la décision**, sans automatisation de décisions critiques.

---

## 🏗️ Architecture globale

Le projet repose sur une architecture **modulaire et conteneurisée**, orchestrée par Docker Compose.

```
Données Open Data
      ↓
Import local (raw / samples)
      ↓
ETL (Docker)
      ↓
Données traitées + historisation
      ↓
Training (v1 / v2)
      ↓
Registry & métriques
      ↓
Serving FastAPI (v1 / v2 + shadow)
```

👉 Une description détaillée est disponible dans `docs/architecture.md`.

---

## 🔄 Pipeline MLOps

### 1️⃣ Données

* Données Open Data (Ville de Paris)
* Import manuel
* Stockage local (`data/raw`, `data/samples`)

### 2️⃣ ETL

* Nettoyage et transformations
* Feature engineering temporel
* Historisation des datasets
* Logs dédiés

📄 Détails : `docs/etl.md`

---

### 3️⃣ Entraînement & retraining

* Modèle v1 : baseline
* Modèle v2 : intégration de la variable **Etat arc** pour gérer la dérive capteur
* Comparaison automatique des performances
* Registry de modèles

📁 Artefacts : `models/`
📄 Docs : `docs/doc_structure_et_echantillon.md`

---

### 4️⃣ Serving & évolution contrôlée

* API FastAPI
* v1 et v2 chargées simultanément
* Shadow testing (`/predict_v2`)
* Bascule et rollback via `active_model.json`
* Logs de serving

📄 Docs : `docs/Serving_3.md`

---

## 🔐 Sécurité, conformité et gouvernance

Le projet intègre dès la conception :

* authentification par **clé API** pour le serving,
* journalisation minimale des accès,
* traçabilité des modèles et des données,
* gouvernance claire du cycle de vie IA.

📄 Documents dédiés :

* `docs/registre_ia.md`
* `docs/gouvernance_ia.md`

---

## 🐳 Docker & exécution

Chaque composant est isolé dans un conteneur Docker :

* ETL
* Training
* Serving
* (Front et API auxiliaires)

L’orchestration est assurée par **Docker Compose**.

📄 Détails : `docs/Docker.md`
📄 Guide pas-à-pas : `docs/run_local.md`

---

## ▶️ Lancer le projet en local (résumé)

```bash
docker compose -p infotraf up -d --build serving
```

Tester l’API :

* `GET /health`
* `POST /predict` (clé API requise)

👉 Voir `docs/run_local.md` pour les commandes complètes.

---

## ⚠️ Difficultés & améliorations futures

Certaines limites ont été identifiées :

* déploiement cloud (AWS) non finalisé,
* absence de HTTPS,
* monitoring avancé non implémenté,
* CI/CD à automatiser.

Ces points sont analysés et documentés dans :
📄 `docs/difficultes_et_ameliorations.md`

---

## 📁 Structure du dépôt (simplifiée)

```
InfoTrafic/
├── app.py
├── data/
├── docker/
├── docker-compose.yml
├── docs/
├── logs/
├── models/
├── serving/
├── src/
└── scripts/
```

---

## ✅ Conclusion

Le projet **InfoTrafic** propose :

* une chaîne MLOps complète et fonctionnelle,
* une gestion réaliste de la dérive des données,
* un serving sécurisé et versionné,
* une documentation claire et structurée.

Il constitue une base solide pour une **industrialisation de l’IA**, tout en restant adaptée à un cadre pédagogique.

---

📌 **Auteurs** : Merveille MAKOUGAN et Maël ZINSOU
📌 **Contexte** : Projet fil rouge – Industrialisation de l’IA dans le Cloud