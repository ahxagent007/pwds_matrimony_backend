#!/bin/sh

echo "Waiting for MySQL to be ready..."
while ! nc -z db 3306; do
  echo "MySQL not ready!"
  sleep 1
done

echo "MySQL is up - starting Django!"
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
