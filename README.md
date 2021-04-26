# Web - 2021

Attention aux permissions du fichier postgres_data afin que docker puisse persister les données dans ce dossier

## Installation

$ docker-compose up --build -d
$ docker exec -it web /bin/sh
$ python manage.py createsuperuser

Connection à la base de données
$ docker exec -it db /bin/sh
$ psql -h db -U postgres

### Initialisation

Étape 1 : open localhost:8000/importation
Une fois que le message "Fin de l'importation" apparait, l'importation se sera bien passée

Étape 2 : open localhost:8000

### Production

## Documentation

## Tests

  
