#!/bin/bash
set -e

echo "=== Starting Django Application ==="
echo "PORT: ${PORT:-8000}"

echo "Running migrations..."
python manage.py migrate || echo "Migration failed, continuing..."

echo "Creating superuser..."
python manage.py createsuperuserauto || echo "Superuser creation skipped (may already exist)"

echo "Loading COMP3003 midterm questions..."
python manage.py load_midterm_questions || echo "COMP3003 midterm questions loading skipped (may already exist)"

echo "Loading SAP midterm questions..."
python manage.py load_sap_midterm_questions || echo "SAP midterm questions loading skipped (may already exist)"

echo "Loading COMP3007 midterm questions..."
python manage.py load_comp3007_midterm_questions || echo "COMP3007 midterm questions loading skipped (may already exist)"

echo "Loading COMP4207 midterm questions..."
python manage.py load_comp4207_midterm_questions || echo "COMP4207 midterm questions loading skipped (may already exist)"

echo "Loading COMP4211 midterm questions..."
python manage.py load_comp4211_midterm_questions || echo "COMP4211 midterm questions loading skipped (may already exist)"

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
