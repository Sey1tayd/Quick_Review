#!/bin/bash
set -e

echo "=== Starting Django Application ==="
echo "PORT: ${PORT:-8000}"

echo "Running migrations..."
python manage.py migrate || echo "Migration failed, continuing..."

echo "Creating superuser..."
python manage.py createsuperuserauto || echo "Superuser creation skipped (may already exist)"

echo "Loading final exam questions..."
python manage.py add_final_questions || echo "Final exam questions loading skipped (may already exist)"

echo "Loading COMP3003 questions..."
python manage.py add_comp3003_questions || echo "COMP3003 questions loading skipped (may already exist)"

echo "Loading COMP4207 questions..."
python manage.py add_comp4207_questions || echo "COMP4207 questions loading skipped (may already exist)"

echo "Loading COMP4211 questions..."
python manage.py add_comp4211_questions || echo "COMP4211 questions loading skipped (may already exist)"

echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Static collection failed, continuing..."

echo "Starting Gunicorn on 0.0.0.0:${PORT:-8000}..."
exec gunicorn quizsite.wsgi \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
