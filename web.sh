#!/bin/sh

# Set up the frontend
cd /frontend
npm run build

# Set up the backend
cd /backend
python manage.py migrate
if [ -f "dump.json" ]; then
    echo "Loading dump.json"
    python manage.py loaddata dump.json
fi
python manage.py collectstatic --noinput

# Run the servers
python manage.py runserver 0.0.0.0:8000 &
cd /frontend && node build