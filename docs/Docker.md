# 🐳 Docker – Conteneurisation du projet InfoTrafic

## 🎯 Objectif

Docker est utilisé dans ce projet pour :

* isoler chaque étape du pipeline (ingestion, ETL, training, serving, front),
* garantir la reproductibilité des exécutions,
* faciliter le déploiement local et cloud,
* standardiser les environnements d’exécution.

Chaque composant est exécuté dans son propre conteneur.

---

## 🧱 Organisation des images Docker

Les images sont définies dans le dossier :

```
docker/
├── Dockerfile.ingest
├── Dockerfile.etl
├── Dockerfile.training
├── Dockerfile.serving
├── Dockerfile.api
└── Dockerfile.front
```

Chaque Dockerfile correspond à **une étape fonctionnelle distincte** du pipeline.

---

## 🔄 Orchestration avec Docker Compose

L’orchestration des conteneurs est assurée par **Docker Compose**, via le fichier :

```
docker-compose.yml
```

Ce fichier permet de :

* définir les dépendances entre services,
* monter les volumes de données et de modèles,
* exposer uniquement les ports nécessaires,
* centraliser la configuration.

---

## 🤖 Service d’entraînement (training)

### Rôle

Le service `training` :

* consomme les données transformées issues de l’ETL,
* entraîne le modèle de machine learning,
* génère les artefacts versionnés (modèles, rapports, registry).

---

### Volumes montés

| Volume hôte        | Volume conteneur | Rôle                 |
| ------------------ | ---------------- | -------------------- |
| `./data/processed` | `/app/processed` | Données d’entrée     |
| `./models`         | `/app/models`    | Modèles et métriques |
| `./logs/training`  | `/app/logs`      | Logs d’entraînement  |

Ces volumes permettent de **persister les résultats hors du conteneur**.

---

### Lancement via Docker Compose

```bash
docker compose up training
```

Le conteneur s’exécute, produit les artefacts, puis se termine.

---

## ▶️ Lancement manuel (optionnel)

Dans certains cas (debug, test isolé), il est possible de construire et lancer manuellement l’image du training.

### Build

```bash
docker build -f docker/Dockerfile.training -t infotraf-training .
```

### Run

```bash
docker run --rm \
  -v "$(pwd)/data/processed:/app/processed" \
  -v "$(pwd)/models:/app/models" \
  -v "$(pwd)/logs/training:/app/logs" \
  infotraf-training
```

Cette méthode est **optionnelle** et n’est pas utilisée dans le flux standard.

---

## 🔐 Bonnes pratiques appliquées

* séparation claire des responsabilités par conteneur,
* aucun secret versionné (variables via `.env`),
* persistance des données et modèles via volumes,
* images spécialisées et légères,
* orchestration centralisée par Docker Compose.

---

## 📌 Conclusion

Docker constitue la brique centrale de l’industrialisation du projet InfoTrafic.
Il permet de garantir :

* la reproductibilité des entraînements,
* la stabilité du serving,
* et la cohérence entre les environnements de développement et de déploiement.