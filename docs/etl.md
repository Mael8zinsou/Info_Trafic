# Pipeline d’ingestion de données

## Objectif du script
Le script `ingest_data.py` a pour objectif de charger un échantillon de données depuis un fichier CSV, vérifier que sa structure correspond aux attentes, et produire un journal d’exécution.  
Cette étape constitue la première brique de l’ingestion des données vers le Data Lake Cloud.

## Source des données
Les données utilisées pour tester le script proviennent d’un **CSV d’échantillon** situé dans :  
```

data/samples/traffic_sample.csv

```
Ce fichier contient un extrait représentatif du dataset complet et sert uniquement aux tests.

## Format et structure du fichier d’échantillon

### Colonnes attendues
- Identifiant arc  
- Libelle  
- Date et heure de comptage  
- Débit horaire  
- Taux d'occupation  
- Etat trafic  
- Identifiant noeud amont  
- Libelle noeud amont  
- Identifiant noeud aval  
- Libelle noeud aval  
- Etat arc  
- Date debut dispo data  
- Date fin dispo data  
- geo_point_2d  
- geo_shape  

### Types principaux
- Texte : `Libelle`, `Etat trafic`, `geo_shape`  
- Numérique : `Débit horaire`, `Taux d'occupation`  
- Date/heure : `Date et heure de comptage`, `Date debut dispo data`, `Date fin dispo data`  
- Géométrie : `geo_point_2d`, `geo_shape`

### Exemple de 3 lignes de l’échantillon

| Identifiant arc | Libelle            | Date et heure de comptage  | Débit horaire | Taux d'occupation | Etat trafic | ... |
|-----------------|------------------|---------------------------|---------------|-----------------|-------------|-----|
| 5462            | AE_A4_bretelle_11 | 2025-11-04T17:00:00+01:00 |               | 5.25            | Fluide      | ... |
| 5462            | AE_A4_bretelle_11 | 2025-11-04T18:00:00+01:00 |               | 5.10            | Fluide      | ... |
| 5462            | AE_A4_bretelle_11 | 2025-11-04T20:00:00+01:00 |               | 29.40           | Pré-saturé  | ... |

> Note : le CSV complet contient toutes les colonnes listées ci-dessus.

## Exécution du script
Pour lancer le script, depuis le dossier `etl/` :

```bash
python3 ingest_data.py
```

### Sortie attendue

* Affichage du nombre de lignes et de colonnes du CSV chargé
* Vérification des colonnes obligatoires
* Création d’un fichier de logs `logs/ingestion.log` contenant :

  * Date et heure du traitement
  * Source des données
  * Résultat des contrôles de structure
  * Succès ou échec de l’ingestion


# Seance 7
on change les données d'entrée, c'est une évolution en pointe
## Contexte
(simulée)
En situation de production, certains arcs deviennent invalides (panne capteur, maintenance, travaux).
Ces arcs continuent de produire des mesures bruitées, ce qui modifie la distribution de certaines variables d’entrée, notamment le taux d’occupation.
## Cause
  * aucune information sur la qualité capteur
  * le modèle interprète du bruit comme du signal
  * hypothèse de stationnarité violée
## Symptômes
  * baisse de l’accuracy globale

  * confusion accrue entre Fluide et Pré-saturé

  * erreurs concentrées sur périodes récentes
## Action
ajout explicite de l’état de validité de l’arc

adaptation du jeu de features

rééquilibrage des classes
## Impact
meilleure robustesse

performance plus stable dans le temps

modèle plus explicable en prod

## lancer le training
* v1 :   python -m src.training.train --dataset dataset_processed.csv --model model_v1.joblib
* v2 :   python -m src.training.train_v2 --dataset traffic_normalized.csv --model model_v2.joblib

## Comparer et tracer
* python -m src.training.compare_models --dataset dataset_retraining_v2.csv

* v1 n’exploite pas Etat arc → il est structurellement moins robuste sur data bruitée

* v2 est conçu pour ça → c’est le but du retraining

## Serving v1 et v2

Shadow + bascule contrôlée :

/predict = modèle actif (v1 au départ)

/predict_v2 = endpoint shadow (toujours v2 pour comparer)

un fichier models/active_model.json pilote la bascule :

{"active":"v1"} → prod v1

{"active":"v2"} → prod v2

rollback = remettre v1 dans le JSON

### Bascule / rollback

Édite models/active_model.json :

bascule prod → {"active":"v2"}

rollback → {"active":"v1"}