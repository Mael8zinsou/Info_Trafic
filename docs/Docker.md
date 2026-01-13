## Docker entraînement
 
Build :

docker build -f docker/Dockerfile.train -t filrouge-train:1.0 .
 
Run :

docker run --rm -v "$(pwd)/data/processed:/app/data/processed" -v "$(pwd)/models:/app/models" filrouge-train:1.0
 
Volumes :

- /app/data/processed : données d’entrée (montées depuis la VM)

- /app/models : sortie modèle (écrite sur la VM)

 