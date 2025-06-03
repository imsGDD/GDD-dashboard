#!/bin/bash
# run migrations
python manage.py migrate

# Start Gunicorn with the desired number of workers and other configurations
exec gunicorn gdd.wsgi:application \
    --name gdd \
    --workers 3 \
    --bind 0.0.0.0:80 \
    --log-level=info \
    --log-file=file.log \
    --access-logfile=access_file.log \
    --reload  # Remove --reload in a production environment