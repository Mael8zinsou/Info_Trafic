# ▶️ Guide d'Exécution Local (Runbook)

Ce document détaille la procédure pour lancer le projet **InfoTrafic**, tester le serving multi-version (v1/v2), valider la sécurité et monitorer les logs.

---

## 1. 🛠 Prérequis

* **Docker & Docker Compose** (obligatoire pour l'isolation).
* **Terminal Bash/ZSH** (WSL2 recommandé pour les utilisateurs Windows).
* **Clé API de test** (définie dans votre `.env`).

Vérifiez votre installation :

```bash
docker compose version

```

---

## 2. ⚙️ Configuration Initiale

Le projet utilise des variables d'environnement pour sécuriser l'accès à l'IA. À la racine du projet :

1. **Création des fichiers :**
```bash
touch .env .env.aws

```


2. **Définition de la clé :** Ouvrez `.env` et ajoutez votre secret :
```env
SERVING_API_KEY=mon_secret_ultra_securise_2026

```



---

## 3. 🚀 Lancement du Service (Serving API)

Nous utilisons Docker pour garantir que le modèle tourne dans le même environnement que celui de son entraînement.

```bash
# Construction et lancement en mode détaché
docker compose -p infotraf up -d --build serving

```

**Vérification de la santé du service :**

```bash
# Vérifier si les containers sont "Up"
docker compose -p infotraf ps

# Consulter les logs de démarrage (important pour le chargement des modèles)
docker compose -p infotraf logs -f serving

```

---

## 4. 🔐 Test de l'API & Sécurité

L'API est protégée. Chaque requête doit inclure le header `X-API-Key`.

### ❌ Test 1 : Accès refusé (Sans clé)

```bash
curl -i -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"Identifiant arc": 12345, "heure": 8, "Taux d\'occupation": 0.42, "lat": 48.85, "lon": 2.35}'
# Résultat attendu : 401 Unauthorized

```

### ✅ Test 2 : Accès autorisé

```bash
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: mon_secret_ultra_securise_2026" \
  -d '{"Identifiant arc": 12345, "heure": 8, "jour_semaine": 1, "is_weekend": 0, "Taux d\'occupation": 0.42, "lat": 48.85, "lon": 2.35, "Etat arc": "ouvert"}'

```

---

## 5. 🌓 Stratégie Multi-Modèles (V1 / V2)

Le système permet de tester un modèle "challenger" (v2) sans interrompre la production (v1).

### Shadow Testing Automatisé

Lancez le container de test pour comparer les deux versions :

```bash
docker compose -p infotraf run --rm tester

```

### Bascule Contrôlée (Blue-Green)

Modifiez dynamiquement le modèle utilisé par l'endpoint `/predict` via le fichier `models/active_model.json` :

* **Pour passer en V2 :** `{"active": "v2"}`
* **Pour un Rollback V1 :** `{"active": "v1"}`

> [!TIP]
> **Pas de redémarrage :** L'API détecte le changement de version sans avoir besoin de relancer le container.

---

## 📁 6. Localisation des Artefacts

| Type | Chemin | Utilité |
| --- | --- | --- |
| **Logs** | `logs/serving/serving.log` | Historique des requêtes et erreurs. |
| **Modèles** | `models/model_v1.joblib` | Binaires des modèles entraînés. |
| **Metrics** | `models/registry.json` | Performance comparée (Accuracy, F1). |
| **Rapports** | `models/report_v2.txt` | Détails de l'entraînement V2. |

---

## 🧹 7. Nettoyage

Pour arrêter proprement les services et libérer les ports :

```bash
docker compose -p infotraf down

```