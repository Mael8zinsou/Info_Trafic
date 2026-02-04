# ⚠️ Difficultés Rencontrées & Axes d’Amélioration

## 🎯 Introduction

Ce document dresse le bilan technique du projet **InfoTrafic**. Loin de masquer les obstacles, il analyse les défis rencontrés durant la phase de développement et définit une feuille de route pour une mise en production à l'échelle industrielle.

---

## 1️⃣ Difficultés Rencontrées (Post-Mortem Technique)

### 1.1 La Gestion du Data Drift (Dérive de Données)

**Le Défi :** Le passage d'un environnement contrôlé (Notebook) à un environnement dynamique (Serving) a révélé la fragilité du modèle V1 face aux pannes capteurs (`Etat arc`).

* **Symptômes :** Chute brutale du  sur la classe "Pré-saturé" lors de l'injection de données bruitées.
* **Analyse :** Violation de l'hypothèse de stationnarité ; le modèle interprétait des erreurs matérielles comme des flux de trafic.
* **Pivot :** Transition vers une architecture V2 incluant une gestion explicite de la qualité de la donnée ().

### 1.2 L'Enfer des Dépendances (Environment Parity)

**Le Défi :** Incompatibilité de sérialisation entre l'environnement de Training et le conteneur de Serving.

* **Erreur :** `AttributeError: '_RemainderColsList' object has no attribute...` liée à un écart de version de `scikit-learn` (1.5.1 vs 1.8.0).
* **Impact :** Crash systémique du service de serving au démarrage.
* **Leçon apprise :** L'importance capitale du verrouillage des versions dans le `requirements.txt` et de l'utilisation d'images de base identiques pour tout le cycle de vie du modèle.

### 1.3 Barrières au Déploiement Cloud (AWS)

**Le Défi :** Difficultés d'accès SSH et de gestion des paires de clés sur l'instance EC2 de staging.

* **Décision :** Arbitrage entre temps de résolution et avancement des briques fonctionnelles.
* **Pivot :** Le déploiement cloud a été gelé au profit d'une **reproductibilité locale parfaite via Docker Compose**, garantissant que le passage au cloud ne soit plus qu'une question de configuration réseau et non de code.

---

## 2️⃣ Axes d’Amélioration (Roadmap 2.0)

### 2.1 Industrialisation du Déploiement (CI/CD)

Pour dépasser le stade du prototype, l'automatisation est la priorité :

* **CI (Continuous Integration) :** Tests unitaires systématiques sur les scripts ETL et validation de schéma à chaque .
* **CD (Continuous Deployment) :** Build automatique des images Docker et déploiement "Canary" sur AWS dès qu'un modèle surpasse les métriques de la Baseline.

### 2.2 Observabilité & Monitoring Avancé

Passer d'une consultation manuelle des logs à un tableau de bord en temps réel :

* **Metrics :** Suivi de la latence d'inférence et du débit de requêtes.
* **Alerting :** Mise en place de seuils (ex: si l'Accuracy tombe sous 85%, une alerte Slack est envoyée).
* **Outils :** Intégration de Prometheus pour la collecte et Grafana pour la visualisation.

### 2.3 Renforcement de la Sécurité

L'authentification simple par clé API est une première étape qui doit évoluer :

* **Gestion des Secrets :** Utilisation d'un coffre-fort numérique (ex: AWS Secrets Manager ou HashiCorp Vault).
* **Identity :** Passage à des jetons **JWT** avec expiration pour limiter les risques en cas de fuite de clé.

### 2.4 Évolution Algorithmique

Le modèle actuel est une base robuste, mais peut être optimisé :

* **Ingénierie Spatiale :** Remplacer le clustering KMeans simple par des modèles de graphes (Graph Neural Networks) pour mieux capturer la connectivité entre les arcs routiers.
* **Auto-Retraining :** Déclenchement automatique d'un nouvel entraînement dès qu'un Drift significatif est détecté par le système de monitoring.

---

## 3️⃣ Conclusion

Les défis rencontrés illustrent la réalité d'un projet MLOps : **80% du travail se situe en dehors du modèle lui-même.**

La priorité a été donnée à la **robustesse architecturale** (Docker, multi-versioning, sécurité) plutôt qu'à la complexité algorithmique. Cette approche garantit que le système InfoTrafic est aujourd'hui "Production-Ready", prêt à évoluer vers une infrastructure Cloud à grande échelle.