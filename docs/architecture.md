# 🏗️ Architecture du Projet : InfoTrafic

## 🎯 Objectifs de la Solution

L’architecture du projet **InfoTrafic** est conçue pour supporter un cycle de vie ML complet, de l'ingestion brute à l'inférence sécurisée. Elle repose sur quatre piliers :

* **Modularité :** Séparation stricte des responsabilités (Ingest, ETL, Train, Serve).
* **Évolutivité :** Capacité à faire cohabiter et comparer des versions de modèles (v1 vs v2).
* **Reproductibilité :** Isolation complète via Docker pour garantir un comportement identique en local et sur le Cloud.
* **Confiance :** Intégration de la sécurité (API Key) et de la gouvernance dès la conception.

---

## 🧱 Vue d’Ensemble du Pipeline

Le projet est orchestré par **Docker Compose**, transformant chaque étape du pipeline en un micro-service autonome.

### Schéma de flux (Data & Model Flow)

```text
      [ Sources ]             [ Traitement ]           [ Apprentissage ]          [ Livraison ]
    ┌─────────────┐         ┌────────────────┐        ┌─────────────────┐       ┌────────────────┐
    │  Ville de   │  Load   │      ETL       │ Train  │    Training     │ Push  │  Serving API   │
    │    Paris    ├────────►│    (Docker)    ├───────►│    (v1 / v2)    ├──────►│   (FastAPI)    │
    │ (Open Data) │         └───────┬────────┘        └────────┬────────┘       └───────┬────────┘
    └─────────────┘                 │                          │                        │
                                    ▼                          ▼                        ▼
                            ┌────────────────┐        ┌─────────────────┐       ┌────────────────┐
                            │ data/processed │        │     models/     │       │    Clients     │
                            │   + history    │        │  (Artifacts)    │       │  (Web/Tester)  │
                            └────────────────┘        └─────────────────┘       └────────────────┘

```

---

## 🔹 Description des Composants

### 1️⃣ Pipeline de Données (ETL)

Le service ETL transforme la donnée brute "sale" en un dataset prêt pour le ML.

* **Entrées :** Fichiers CSV dans `data/raw/`.
* **Traitements :** Nettoyage, feature engineering temporel, extraction GPS (lat/lon).
* **Persistance :** Les données transformées sont versionnées dans `data/processed/history/` pour permettre le "Time Travel" et l'analyse de drift.

### 2️⃣ Engine d'Entraînement (Training)

Ce composant gère la logique de modélisation et la comparaison.

* **Multi-Version :** Supporte l'entraînement de la **v1** (baseline) et de la **v2** (robuste au drift).
* **Registre :** Génère un fichier `registry.json` contenant les métriques de performance, servant de référence à l'API de serving.

### 3️⃣ Serving & Inférence (API IA)

Le service le plus critique, conçu pour la haute disponibilité et la mise à jour transparente.

* **Shadow Ingress :** Capacité à router les requêtes vers le modèle de production ou le modèle "challenger".
* **Bascule Contrôlée :** Utilisation d'un commutateur dynamique (`active_model.json`) pour le **Blue-Green Deployment**.

---

## 🐳 Orchestration & Sécurité

### Isolation Docker

Chaque brique possède son propre `Dockerfile`, garantissant que les dépendances (ex: versions de `scikit-learn`) ne créent pas de conflits entre le training et le serving.

* **Réseau :** Un réseau interne Docker (`ml-network`) isole les communications.
* **Volumes :** Montage de volumes pour la persistance des modèles et des logs sans alourdir les images.

### Gouvernance & Sécurité

* **Authentification :** Protection périmétrale par `X-API-Key`.
* **Traçabilité :** Journaux d'exécution centralisés dans le dossier `logs/`.
* **Audit :** Registre des modèles pour suivre l'évolution des performances dans le temps.

---

## ☁️ Vers une Infrastructure Cloud

Bien que le projet soit actuellement validé en local/staging, l'architecture est **Cloud-Native** :

1. **Portabilité :** Les Dockerfiles sont prêts pour **AWS ECR** (Elastic Container Registry).
2. **Déploiement :** Compatible avec **AWS EC2** ou **ECS** (Elastic Container Service).
3. **Sécurité :** Prêt pour une intégration avec des Secrets Managers pour la gestion des clés API.

---

## ✅ Conclusion

Cette architecture ne se contente pas de "faire tourner un modèle" ; elle crée un écosystème où le changement est maîtrisé. La séparation claire entre le **code**, la **donnée** et le **modèle** permet une amélioration continue sans rupture de service, pilier fondamental de la culture MLOps.