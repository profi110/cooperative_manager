#!/bin/sh

# Очікування готовності бази даних
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Виконання міграцій для всіх додатків (users, meters тощо)
python manage.py migrate --noinput

# Збір статики для WhiteNoise
python manage.py collectstatic --noinput

exec "$@"