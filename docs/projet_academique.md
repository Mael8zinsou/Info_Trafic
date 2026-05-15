# 🎓 Contexte académique — Projet Fil Rouge

> Cette page conserve la présentation académique du projet. Pour une vision portfolio (architecture, démo, stack technique), voir le [README principal](../README.md).

---

## Objectif du projet

**InfoTrafic** est un projet fil rouge visant à concevoir une **chaîne MLOps complète**, de la donnée brute jusqu'au serving sécurisé d'un modèle de machine learning.

Le projet met l'accent sur :

* la **robustesse du pipeline**,
* la **gestion de la dérive des données**,
* l'**évolution contrôlée des modèles**,
* la **sécurité, la conformité et la gouvernance de l'IA**.

Il s'inscrit dans un cadre académique (YNOV — Industrialisation de l'IA dans le Cloud), avec une approche réaliste inspirée de contextes industriels.

---

## Cas d'usage

À partir de données Open Data issues de capteurs routiers parisiens, le système prédit l'**état du trafic** (Fluide / Pré-saturé / Saturé / Bloqué) pour un segment routier donné, en fonction de :

* l'heure et le jour,
* le taux d'occupation,
* la localisation (lat/lon),
* l'état de validité du capteur (`Etat arc`).

Le système agit comme **une aide à la décision**, sans automatisation de décisions critiques.

---

## Pipeline MLOps

### 1️⃣ Données

* Données Open Data (Ville de Paris)
* Import manuel
* Stockage local (`data/raw`, `data/samples`)

### 2️⃣ ETL

* Nettoyage et transformations
* Feature engineering temporel (heure, jour_semaine, is_weekend)
* Extraction lat/lon depuis `geo_point_2d`
* Historisation des datasets dans `data/processed/history/`
* Auto-détection de l'encodage CSV (UTF-8 BOM / UTF-8 / ISO-8859-1)

📄 Détails : [etl.md](etl.md)

### 3️⃣ Entraînement & retraining

* **Modèle v1** : baseline (LogisticRegression, sans `Etat arc`)
* **Modèle v2** : intégration de la variable **`Etat arc`** pour gérer la dérive capteur
* Comparaison automatique des performances
* Registry de modèles avec métriques et chemins relatifs

📁 Artefacts : `models/`
📄 Docs : [doc_structure_et_echantillon.md](doc_structure_et_echantillon.md)

### 4️⃣ Serving & évolution contrôlée

* API FastAPI multi-version
* v1 et v2 chargées simultanément en mémoire
* Shadow testing via `/predict_v2`
* Bascule blue-green et rollback via `active_model.json` (sans redémarrage)
* Logs de serving structurés

📄 Docs : [serving_api.md](serving_api.md)

---

## Sécurité, conformité et gouvernance

Le projet intègre dès la conception :

* authentification par **clé API** (header `x-api-key`) pour le serving,
* journalisation minimale des accès,
* traçabilité des modèles et des données via le registry,
* gouvernance claire du cycle de vie IA.

📄 Documents dédiés :

* [registre_ia.md](registre_ia.md)
* [gouvernance_ia.md](gouvernance_ia.md)

---

## Difficultés & améliorations identifiées

Certaines limites ont été reconnues et documentées :

* déploiement cloud (AWS) non finalisé,
* absence de HTTPS,
* CI/CD initialement minimaliste (depuis enrichie : tests + smoke + monitoring).

📄 Analyse complète : [difficultes_et_ameliorations.md](difficultes_et_ameliorations.md)

---

## Conclusion académique

Le projet **InfoTrafic** propose :

* une chaîne MLOps complète et fonctionnelle,
* une gestion réaliste de la dérive des données,
* un serving sécurisé et versionné,
* une documentation claire et structurée,
* une observabilité industrielle (Prometheus + Grafana) ajoutée en post-soutenance.

Il constitue une base solide pour une **industrialisation de l'IA**, tout en restant adaptée à un cadre pédagogique.

---

📌 **Contexte** : Projet fil rouge — YNOV, Industrialisation de l'IA dans le Cloud
