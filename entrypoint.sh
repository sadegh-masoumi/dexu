#!/bin/sh

# Wait for database to be ready
echo "Waiting for Postgres..."
while ! nc -z db 5432; do
  sleep 0.5
done
echo "Postgres is ready"

# Apply migrations and run server
python manage.py migrate
python manage.py collectstatic --noinput

uvicorn core.asgi:application --host 0.0.0.0 --port 8000
