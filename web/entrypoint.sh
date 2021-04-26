#!/bin/sh

python manage.py makemigrations
python manage.py flush --no-input
python manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('root', 'root@root.com', 'root')" | python manage.py shell

exec "$@"

python importation.py
