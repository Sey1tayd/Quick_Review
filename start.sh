#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
python manage.py createsuperuserauto || echo "Superuser creation skipped (may already exist)"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn quizsite.wsgi --bind 0.0.0.0:${PORT:-8000} --log-file - --access-logfile - --error-logfile -
