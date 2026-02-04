# Registre IA – Projet InfoTrafic

## 1. Identification du système
- Nom du système : InfoTrafic – Prédiction de l’état du trafic
- Type : Système d’aide à la décision basé sur un modèle de machine learning
- Responsable : Équipe Data / IA (projet académique – fil rouge)

## 2. Finalité du traitement
Le système vise à prédire l’état du trafic routier (Fluide, Pré-saturé, Saturé, Bloqué) à partir de mesures issues de capteurs de trafic.
Il s’agit d’un outil d’aide à la décision, sans automatisation de décisions critiques.

## 3. Données utilisées
- Identifiant d’arc
- Date et heure de comptage (transformée en variables temporelles)
- Taux d’occupation
- Débit horaire
- État de l’arc (Ouvert / Invalide / Barré)
- Localisation géographique (latitude / longitude)

Aucune donnée directement personnelle n’est utilisée (pas de nom, pas d’identifiant individuel).

## 4. Données sensibles et vigilance
Les données de localisation (latitude / longitude) peuvent être considérées comme sensibles dans certains contextes.
Dans ce projet :
- elles sont utilisées uniquement à des fins de prédiction du trafic,
- elles ne permettent pas l’identification directe d’une personne,
- aucun recoupement avec des données personnelles n’est effectué.

## 5. Principes RGPD appliqués
- Finalité : usage strictement limité à la prédiction du trafic.
- Minimisation : seules les variables nécessaires au modèle sont conservées.
- Transparence : modèle explicable et features connues.
- Conservation limitée : datasets et modèles sont versionnés, sans conservation illimitée.

## 6. Traçabilité et journalisation
Le système met en place une journalisation minimale :
- Logs ETL : transformations et volumes de données (`logs/etl.log`)
- Logs training : datasets utilisés, métriques et artefacts (`logs/training.log`)
- Versionnement des modèles : `model_v1`, `model_v2`
- Registre des performances : `registry.json`, `comparison_v1_v2.csv`
- Logs serving : accès, statut des requêtes et version de modèle (sans stockage des données brutes)

## 7. Explicabilité
Le modèle repose sur une régression logistique intégrée dans un pipeline scikit-learn.
Les variables utilisées sont connues et interprétables.

## 8. Conclusion
Le système InfoTrafic respecte les principes fondamentaux de conformité attendus pour un projet d’IA académique :
- absence de données personnelles directes,
- usage maîtrisé et justifié,
- traçabilité des traitements et des décisions.
