# Gouvernance de l’IA – Projet InfoTrafic

## 1. Objectifs de la gouvernance
La gouvernance du système IA vise à :
- garantir un usage maîtrisé et sécurisé du modèle,
- encadrer les évolutions du système,
- permettre un retrait ou un rollback rapide en cas d’incident.

## 2. Rôles et responsabilités
Même si le projet est réalisé dans un cadre académique, les rôles sont clairement identifiés :

### Rôle Data / IA
- préparation et transformation des données,
- entraînement et évaluation des modèles,
- analyse des performances et détection de dérives,
- préparation des nouvelles versions du modèle.

### Rôle IT / Ops
- déploiement des services (Docker, API),
- gestion de la sécurité de l’API (clé d’accès),
- supervision technique et gestion des logs,
- mise en œuvre du rollback si nécessaire.

### Rôle Métier
- définition de la finalité du système,
- validation fonctionnelle des résultats,
- décision de mise en production ou de retrait d’un modèle.

## 3. Cycle de vie du modèle
1. Ingestion et ETL produisent un dataset traité (`dataset_processed_current.csv`).
2. Entraînement du modèle et génération des artefacts.
3. Comparaison entre versions (v1 / v2) à l’aide de métriques.
4. Exposition du nouveau modèle en mode shadow (`/predict_v2`).
5. Bascule contrôlée via le fichier `active_model.json`.

## 4. Bascule et rollback
- Le modèle actif est défini par `models/active_model.json`.
- La bascule entre versions est immédiate et ne nécessite pas de redéploiement.
- En cas d’incident, le rollback consiste à réactiver la version précédente.

## 5. Gestion des incidents IA
Les incidents peuvent être déclenchés par :
- des erreurs récurrentes côté API,
- une baisse de performance constatée,
- des comportements inattendus du modèle.

Procédure :
1. Analyse des logs (serving, training).
2. Retour immédiat vers une version stable du modèle.
3. Analyse des causes (données, dérive, configuration).
4. Correction et éventuel retraining.
5. Documentation de l’incident.

## 6. Supervision humaine
Le système IA agit comme une aide à la décision.
Une supervision humaine est toujours possible, et aucune décision critique n’est prise automatiquement par le modèle.

## 7. Conclusion
La gouvernance du projet InfoTrafic repose sur :
- une séparation claire des rôles,
- un cycle de vie maîtrisé des modèles,
- des mécanismes de contrôle, de bascule et de retrait rapides.
