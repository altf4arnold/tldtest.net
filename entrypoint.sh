#!/bin/sh

python manage.py makemigrations # Make migrations
python manage.py migrate # Apply database migrations
python manage.py collectstatic


exec "$@"