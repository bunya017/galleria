#! /usr/bin/env bash
# Run collect static and migrations
python galleria/manage.py collectstatic --noinput
python galleria/manage.py migrate
gunicorn galleria.galleria.wsgi --bind=0.0.0.0:80
