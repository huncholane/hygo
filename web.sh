#!/bin/sh

cd frontend && npm start &
cd /backend
python manage.py migrate
if [ -f "dump.json" ]; then
    python manage.py loaddata dump.json
fi
python manage.py collectstatic --noinput

cd /frontend && serve
python manage.py runserver 0.0.0.0:8000