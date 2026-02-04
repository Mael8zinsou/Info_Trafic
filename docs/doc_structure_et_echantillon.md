# 📄 Documentation – Structure des Données & Fichier d’Échantillon
## 🎯 Objectif

Cette documentation présente :

* la **structure des données** utilisées dans le projet,
* les **fichiers d’échantillons** stockés localement,
* les **colonnes attendues** et leurs types,
* les **contrôles effectués avant traitement**,
* le **cadre légal** autorisant l’utilisation de ces données.

Elle constitue la référence pour la compréhension et la validation des données **avant l’étape ETL**.

---

## 🗂️ 1. Source des données

Les données utilisées proviennent du jeu **« Comptage routier – Données trafic issues des capteurs permanents »**, publié par la Ville de Paris via la plateforme **opendata.paris.fr**.

👉 Lien officiel :
[https://opendata.paris.fr](https://opendata.paris.fr)

Ce jeu de données contient des mesures horaires de trafic collectées par des capteurs fixes situés sur le réseau routier parisien.

Dans le cadre de ce projet :

* les données sont **téléchargées manuellement** depuis la plateforme Open Data,
* puis placées dans le dépôt local (`data/raw/` ou `data/samples/`) pour traitement.

Aucune ingestion automatique depuis une API ou un stockage cloud externe n’est mise en œuvre à ce stade.

---

## ⚖️ 2. Base légale (Open Data / RGPD)

Ces données :

* ne contiennent **aucune donnée personnelle**,
* sont publiées sous la **licence Open Data** de la Ville de Paris,
* peuvent être librement réutilisées à des fins d’analyse, d’étude ou d’enseignement.

### Base légale applicable

* Article L.321-1 du **Code des relations entre le public et l’administration (CRPA)**
* Politique *Open Data by default* de la Ville de Paris
* Absence de données à caractère personnel → **RGPD non applicable** (article 2.1)

📌 **Conclusion**
L’utilisation de ces données dans le cadre du projet fil rouge est pleinement légale et ne nécessite aucune anonymisation ou déclaration spécifique.

---

## 📦 3. Colonnes du dataset source (données brutes)

Lors de l’import local des données, **l’intégralité des colonnes du fichier Open Data est conservée**, sans transformation.

Cette approche respecte un principe fondamental en data engineering :

> 🧠 La donnée brute doit être conservée intacte afin de garantir traçabilité, auditabilité et reproductibilité.

| Colonne                   | Type        | Description                                |
| ------------------------- | ----------- | ------------------------------------------ |
| Identifiant arc           | int         | Identifiant du segment routier             |
| Libelle                   | string      | Nom du tronçon                             |
| Date et heure de comptage | datetime    | Horodatage de la mesure                    |
| Débit horaire             | float       | Volume de trafic                           |
| Taux d'occupation         | float       | Pourcentage d’occupation                   |
| Etat trafic               | string      | État global du trafic                      |
| Identifiant noeud amont   | int         | Nœud amont du réseau                       |
| Libelle noeud amont       | string      | Libellé du nœud amont                      |
| Identifiant noeud aval    | int         | Nœud aval du réseau                        |
| Libelle noeud aval        | string      | Libellé du nœud aval                       |
| Etat arc                  | string      | État du tronçon (ouvert, invalide, barré…) |
| Date debut dispo data     | date        | Début de disponibilité                     |
| Date fin dispo data       | date        | Fin de disponibilité                       |
| geo_point_2d              | string      | Coordonnées GPS (lat, lon)                 |
| geo_shape                 | string/JSON | Géométrie du tronçon                       |

---

## 🧹 4. Évolution des colonnes (étape ETL)

Aucune colonne n’est supprimée ou modifiée lors de la phase d’import local.

Les transformations suivantes sont réalisées **uniquement lors de l’étape ETL** :

* extraction de `lat` et `lon` depuis `geo_point_2d`,
* création de variables temporelles (`heure`, `jour_semaine`, `is_weekend`),
* suppression de colonnes non nécessaires au modèle (`geo_shape`, métadonnées),
* nettoyage des valeurs textuelles,
* sélection finale des features utilisées par le modèle.

Cela garantit une séparation claire entre :

* **données sources**,
* **données transformées**,
* **features de modélisation**.

---

## 📝 5. Fichiers d’échantillons

Des fichiers d’échantillons sont fournis dans :

```
data/samples/
```

Exemples :

* `traffic_sample.csv`
* `traffic_sample_last.csv`

Ces fichiers permettent :

* de tester le pipeline ETL,
* de valider la structure des données,
* de reproduire les traitements sans manipuler l’ensemble du dataset.

---

## 🔍 6. Contrôles réalisés avant traitement

Les contrôles sont volontairement **non bloquants**, l’objectif étant de détecter les anomalies sans interrompre le pipeline.

### Contrôles principaux

* lecture correcte du fichier CSV (séparateur, encodage),
* présence des colonnes attendues,
* cohérence des types (numériques / textuels),
* détection de valeurs manquantes,
* vérification de plages plausibles (taux d’occupation, débit).

Les anomalies détectées sont consignées dans les **logs ETL**, sans rejet automatique du fichier.

---

## 📁 7. Organisation des données dans le projet

```
data/
├── raw/            # données brutes téléchargées
├── samples/        # échantillons pour tests
└── processed/      # données transformées (ETL)
    └── history/    # versions historisées
```

Cette organisation facilite :

* le versionnement des données traitées,
* l’analyse de dérive,
* la reproductibilité des entraînements.

---

## 🔐 8. Gestion du dépôt Git

Les éléments suivants sont exclus du versionnement :

```
.env
logs/
data/raw/
```

Objectifs :

* éviter toute fuite de variables sensibles,
* ne pas versionner de données volumineuses,
* maintenir un dépôt propre et exploitable.