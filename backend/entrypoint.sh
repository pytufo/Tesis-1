#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for postgres..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"

  echo "Aplliying migrations..."
  python manage.py makemigrations
  python manage.py migrate

  echo "from accounts.models import User; User.objects.create_superuser('admin@mail.com', 'adminpassword')" | python manage.py shell
  echo "Migrations created succesfully"
fi

#python manage.py flush --no-input

exec "$@"
