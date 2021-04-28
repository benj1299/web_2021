
# Web - 2021

  

Attention aux permissions du fichier postgres_data afin que docker puisse persister les données dans ce dossier

  

## Installation

 

Exécutez toutes les cellules du fichier **analyse.ipynb** avant de commencer 
(permet de générer les fichiers csv pour notre base de données)
  
**Démarrage du serveur**

$ docker-compose up --build -d

**Connection à la base de données**

$ docker exec -it db /bash

$ psql -h db -U postgres
  

**Identifiant de l'administration** (/admin)

Login : root

Mot de passe : root

  

### Initialisation

 1. open localhost:8000/importation
 2. open localhost:8000

Une fois que le message "Fin de l'importation" apparait, l'importation se sera bien passée
 
  

## Documentation

  

## Tests

$ docker exec -it web python manage.py test