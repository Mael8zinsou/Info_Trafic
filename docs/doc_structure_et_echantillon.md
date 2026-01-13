# 📄 Documentation – Structure des Données & Fichier d’Échantillon

*Axée sur (Rôle : Personne 2 – Schéma & Arborescence)*

## 🎯 Objectif

Cette documentation présente :

* La **structure des données** retenues pour le projet.
* Le **fichier d’échantillon** situé dans `data/samples/`.
* Les **colonnes attendues** et leurs types.
* Les **contrôles effectués lors de l’ingestion**.
* La **base légale** permettant l’utilisation de ces données dans le cadre du projet.

Elle constitue la référence officielle pour la bonne exécution de l’étape d’ingestion.

---

## 🗂️ 1. Source des données

Les données utilisées proviennent du jeu **« Comptage routier – Données trafic issues des capteurs permanents »**, publié par la Ville de Paris via la plateforme *opendata.paris.fr*.

👉 **Lien officiel** : [https://opendata.paris.fr](https://opendata.paris.fr)

Ce dataset contient les mesures horaires de trafic enregistrées par des capteurs permanents situés sur le réseau routier parisien.

---

## ⚖️ 2. Base légale (RGPD / Open Data)

Ces données :

* **ne contiennent aucune donnée personnelle**,
* sont mises à disposition sous la **licence Open Data** de la Ville de Paris,
* peuvent être librement réutilisées à des fins d’analyse, d’étude ou d’enseignement.

### **Base légale applicable :**

➡️ **Article L. 321-1 du Code des Relations entre le Public et l’Administration (CRPA)** : réutilisation libre des informations publiques.
➡️ **Décision d’ouverture des données de la Ville de Paris** (Open Data by default).
➡️ Aucun traitement de données à caractère personnel → **RGPD non applicable** (article 2, paragraphe 1).

📌 **Conclusion :** La réutilisation de ce dataset dans le cadre du projet fil rouge est **pleinement légale** et ne nécessite aucune anonymisation supplémentaire.

---


## 📦 3. Colonnes retenues pour le projet *(ingestion : conserver toutes les colonnes brutes)*

Lors de l’ingestion, **toutes les colonnes du dataset original sont conservées**, sans transformation.
Cette approche respecte le principe MLOps suivant :

> 🧠 **L’ingestion doit préserver l’intégrité de la donnée brute pour garantir traçabilité, auditabilité et reproductibilité.**

Ainsi, les colonnes conservées sont :

| Colonne                     | Type        | Description                                   |
| --------------------------- | ----------- | --------------------------------------------- |
| `Identifiant arc`           | int         | Identifiant du segment routier.               |
| `Libelle`                   | string      | Nom du tronçon routier.                       |
| `Date et heure de comptage` | datetime    | Horodatage de la mesure.                      |
| `Débit horaire`             | float       | Volume de trafic observé.                     |
| `Taux d'occupation`         | float       | Pourcentage d’occupation de la voie.          |
| `Etat trafic`               | string      | Statut global du trafic.                      |
| `Identifiant noeud amont`   | int         | Identifiant du nœud amont du réseau.          |
| `Libelle noeud amont`       | string      | Libellé du nœud amont.                        |
| `Identifiant noeud aval`    | int         | Identifiant du nœud aval du réseau.           |
| `Libelle noeud aval`        | string      | Libellé du nœud aval.                         |
| `Etat arc`                  | string      | État du tronçon (ouvert/fermé…).              |
| `Date debut dispo data`     | date        | Période de disponibilité des données — début. |
| `Date fin dispo data`       | date        | Période de disponibilité des données — fin.   |
| `geo_point_2d`              | string      | Coordonnées GPS du capteur (lat,long).        |
| `geo_shape`                 | string/JSON | Forme géométrique du segment routier.         |

### Pourquoi conserver tout ?

* Garantir la **fidélité complète** au fichier brut.
* Laisser la liberté aux futures étapes (ETL, feature engineering) de choisir les colonnes utiles.
* Faciliter les audits et analyses en cas d'anomalies.
* Ne jamais altérer le "raw layer" du data lake.
---

## 🧹 4. Colonnes retirées *(après ingestion, dans l’étape ETL uniquement)*

⚠️ **AUCUNE colonne n’est retirée lors de l’ingestion.**
L’ingestion a pour rôle de **stocker la donnée telle qu’elle existe** dans le Data Lake (S3).

Les suppressions/modifications suivantes seront effectuées **lors de l’étape ETL**, et non lors de l’ingestion :

| Colonne retirée en ETL  | Raison prévue                                            |
| ----------------------- | -------------------------------------------------------- |
| `geo_shape`             | JSON complexe difficile à exploiter sans transformation. |
| `geo_point_2d`          | Peu utile pour un modèle temporel simple.                |
| `Date debut dispo data` | Métadonnée historique.                                   |
| `Date fin dispo data`   | Idem.                                                    |
| Nœuds amont/aval        | À évaluer selon la modélisation.                         |

---

## 📝 5. Fichier d’échantillon

Un fichier de validation a été placé dans :

```
data/samples/sample_trafic.csv
```

Il contient un petit ensemble représentatif du dataset final pour permettre :

* la validation du script d’ingestion,
* les tests de structure,
* la génération des logs.

### Exemple de contenu :

```csv
Identifiant arc;Libelle;Date et heure de comptage;Débit horaire;Taux d'occupation;Etat trafic;Identifiant noeud amont;Libelle noeud amont;Identifiant noeud aval;Libelle noeud aval;Etat arc;Date debut dispo data;Date fin dispo data;geo_point_2d;geo_shape
5462;AE_A4_bretelle_11;2025-11-04T17:00:00+01:00;;5.25;Fluide;2865;A4W;3156;Bercy_bretelles_7-11;Ouvert;1996-11-07;2023-01-01;48.82639270403309, 2.3922636521497997;"{""coordinates"": [[2.392472238153124, 48.82564016646078], [2.392089926647914, 48.82636848688473], [2.3921779059713386, 48.82677282393933], [2.3925203327652027, 48.827080538995425]], ""type"": ""LineString""}"
5462;AE_A4_bretelle_11;2025-11-04T18:00:00+01:00;;5.1;Fluide;2865;A4W;3156;Bercy_bretelles_7-11;Ouvert;1996-11-07;2023-01-01;48.82639270403309, 2.3922636521497997;"{""coordinates"": [[2.392472238153124, 48.82564016646078], [2.392089926647914, 48.82636848688473], [2.3921779059713386, 48.82677282393933], [2.3925203327652027, 48.827080538995425]], ""type"": ""LineString""}"
5462;AE_A4_bretelle_11;2025-11-04T20:00:00+01:00;;29.4;Pré-saturé;2865;A4W;3156;Bercy_bretelles_7-11;Ouvert;1996-11-07;2023-01-01;48.82639270403309, 2.3922636521497997;"{""coordinates"": [[2.392472238153124, 48.82564016646078], [2.392089926647914, 48.82636848688473], [2.3921779059713386, 48.82677282393933], [2.3925203327652027, 48.827080538995425]], ""type"": ""LineString""}"
5462;AE_A4_bretelle_11;2025-11-04T21:00:00+01:00;;19.7;Pré-saturé;2865;A4W;3156;Bercy_bretelles_7-11;Ouvert;1996-11-07;2023-01-01;48.82639270403309, 2.3922636521497997;"{""coordinates"": [[2.392472238153124, 48.82564016646078], [2.392089926647914, 48.82636848688473], [2.3921779059713386, 48.82677282393933], [2.3925203327652027, 48.827080538995425]], ""type"": ""LineString""}"
5462;AE_A4_bretelle_11;2025-11-04T22:00:00+01:00;;3.15;Fluide;2865;A4W;3156;Bercy_bretelles_7-11;Ouvert;1996-11-07;2023-01-01;48.82639270403309, 2.3922636521497997;"{""coordinates"": [[2.392472238153124, 48.82564016646078], [2.392089926647914, 48.82636848688473], [2.3921779059713386, 48.82677282393933], [2.3925203327652027, 48.827080538995425]], ""type"": ""LineString""}"
```

---

## 🔍 6. Contrôles effectués lors de l’ingestion

Étant donné que toutes les colonnes sont conservées, les contrôles portent principalement sur :

### ✔ Contrôles obligatoires

1. **Présence de toutes les colonnes du fichier brut**

   * Le script compare l’en-tête du CSV avec la liste officielle du dataset Open Data.
   * Si une colonne manque → *ingestion refusée*.

2. **Lecture correcte (encoding & parsing)**

   * Spécifiquement requis à cause des colonnes comme `geo_shape` contenant du JSON et des guillemets échappés.

3. **Format du fichier conforme (séparateur ; ou , selon la source)**

   * Le script détecte automatiquement le séparateur ou l’impose selon les besoins.

4. **Structure du dossier d’ingestion respectée**

   * Fichier stocké dans `data/samples/`
   * Logs dans `logs/`
   * Résultat envoyé dans `s3://bucket/raw/YYYY-MM-DD/fichier.csv`

---

### ⚠️ Contrôles facultatifs

Ces contrôles n’arrêtent *pas* le processus, mais génèrent des **warnings** dans les logs :

* Colonnes supplémentaires (non listées par Open Data).
* Valeurs manquantes (`NaN`).
* Valeurs non parsables (surtout dans `geo_shape`).
* Débit horaire négatif ou aberrant.
* Taux d’occupation hors `[0, 100]`.

---

### Exemple de log attendu

```
2025-02-07 15:45:21 - INFO - Lecture du fichier sample_trafic.csv
2025-02-07 15:45:21 - INFO - Colonnes attendues : 15. Colonnes trouvées : 15.
2025-02-07 15:45:21 - INFO - Données brutes conformes : ingestion autorisée.
2025-02-07 15:45:21 - INFO - Upload vers S3 : s3://Info_Trafic/raw/2025-02-07/sample_trafic.csv
```

---

## 📁 7. Arborescence du projet

```
Info_Trafic/
├── data/
│   ├── samples/          # échantillons
│   └── raw/              # données brutes (non versionnées)
├── etl/
│   └── ingest_data.py
├── logs/                 # journaux (exclus du repo)
├── .env                  # variables sensibles (exclu)
├── docs/
│   └── etl.md
└── README.md
```

---

## 🔐 8. Configuration Git

```
.env
logs/
data/raw/
```

Objectifs :

* éviter toute fuite de clés AWS,
* éviter de versionner des fichiers volumineux,
* maintenir un dépôt propre et professionnel.

---