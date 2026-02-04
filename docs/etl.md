# 📑 Documentation Pipeline & Stratégie MLOps

## 1. Ingestion des Données (Baseline)

L'étape d'ingestion sécurise l'entrée des données dans le système et garantit la conformité du schéma avant tout traitement.

* **Script :** `ingest_data.py`
* **Source :** `data/samples/traffic_sample.csv` (échantillon représentatif).
* **Objectif :** Vérifier la structure, les types, et logger l'état de l'import.

### 📋 Schéma de Données (Extraits)

| Colonne | Type | Description |
| --- | --- | --- |
| `Identifiant arc` | Numérique | ID unique du capteur |
| `Date et heure...` | DateTime | Horodatage du comptage |
| `Taux d'occupation` | Numérique | **Variable Cible (Target)** |
| `Etat arc` | Texte | État du capteur (**Ouvert / Invalide**) |
| `geo_point_2d` | Géo | Coordonnées pour le clustering spatial |

**Monitoring :** Un fichier `logs/ingestion.log` est généré à chaque exécution pour tracer le succès ou l'échec des contrôles.

---

## 2. Séance 7 : Simulation de Drift & Évolution

Cette étape simule un cas réel de **Covariate Drift** (changement de la distribution des variables d'entrée).

### ⚠️ Le Problème : Arcs Invalides

En production, la proportion d'arcs en panne (**Etat arc = Invalide**) augmente, injectant du bruit massif.

* **Cause :** Le modèle V1 interprète le bruit des capteurs défectueux comme du signal réel.
* **Symptômes :** Baisse de l'accuracy globale, confusion accrue entre les classes *Fluide* et *Pré-saturé*.
* **Action :** Création d'un pipeline V2 exploitant explicitement l'état de validité et un encodage robuste.

---

## 3. Stratégie d'Entraînement

Nous gérons deux versions du modèle pour assurer la transition et la comparaison.

* **V1 (Baseline) :** Entraînement classique sans gestion du bruit capteur.
```bash
python -m src.training.train --dataset dataset_processed.csv --model model_v1.joblib

```


* **V2 (Robuste) :** Intègre les correctifs de la Séance 7 (features normalisées, gestion `Etat arc`).
```bash
python -m src.training.train_v2 --dataset traffic_normalized.csv --model model_v2.joblib

```



**Comparaison :** Le script `compare_models.py` permet de valider que la V2 surpasse la V1 sur les données bruitées.

---

## 4. Serving & Déploiement (Production)

L'architecture de serving permet une transition sans interruption de service (**Zero Downtime**).

### 🚀 Stratégie de Bascule (Blue-Green)

Le choix du modèle actif est piloté par un fichier de configuration dynamique : `models/active_model.json`.

* **Endpoint `/predict` :** Utilise la version définie comme `"active"` dans le JSON.
* **Endpoint `/predict_v2` :** Toujours dirigé vers la V2 (Shadow Testing) pour monitoring.
* **Rollback :** Pour revenir à la V1, il suffit de modifier le JSON sans redémarrer le serveur.

### 🐳 Docker & Reproductibilité

Le projet utilise deux configurations pour garantir la parité des environnements :

1. **Local :** Pour le développement et le test unitaire.
2. **AWS :** Pour l'exposition externe et le staging.

**Commandes utiles :**

```bash
# Lancer le service de serving (Nom de projet : infotraf)
docker compose -p infotraf up -d --build serving

# Lancer le Shadow Test (Vérification V1 vs V2)
docker compose -p infotraf run --rm tester

```

---

## 🛠️ Maintenance & Troubleshooting

> [!IMPORTANT]
> **Alerte Compatibilité Scikit-Learn**
> Les modèles (`.joblib`) sont sensibles aux versions de bibliothèque.
> * **Erreur :** `_RemainderColsList` au startup.
> * **Cause :** Différence entre la version de training (1.5.1) et celle du container (1.8.0).
> * **Solution :** Toujours aligner le `requirements.txt` du container sur l'environnement de training.