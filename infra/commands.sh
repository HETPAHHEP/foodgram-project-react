#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input --clear

python manage.py import_ingredients_json --no-input