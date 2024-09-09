#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirement.txt

python manage.py collectstatic --no-input --clear
python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate