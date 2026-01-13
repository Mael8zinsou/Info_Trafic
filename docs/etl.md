# Pipeline d’ingestion de données

## Objectif du script
Le script `ingest_data.py` a pour objectif de charger un échantillon de données depuis un fichier CSV, vérifier que sa structure correspond aux attentes, et produire un journal d’exécution.  
Cette étape constitue la première brique de l’ingestion des données vers le Data Lake Cloud.

## Source des données
Les données utilisées pour tester le script proviennent d’un **CSV d’échantillon** situé dans :  
```

data/samples/traffic_sample.csv

````
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
````

### Sortie attendue

* Affichage du nombre de lignes et de colonnes du CSV chargé
* Vérification des colonnes obligatoires
* Création d’un fichier de logs `logs/ingestion.log` contenant :

  * Date et heure du traitement
  * Source des données
  * Résultat des contrôles de structure
  * Succès ou échec de l’ingestion
