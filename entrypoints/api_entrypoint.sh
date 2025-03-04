#!/bin/bash

function cleanup_demodb {
    local demodb_path=/src/demo-db.sqlite3
    if [[ -e $demodb_path ]]; then
        echo "Cleaning up demo db $demodb_path..."
        rm -f $demodb_path
    fi
}

trap cleanup_demodb SIGTERM
trap cleanup_demodb SIGINT

echo "Starting Migrations"
python3 manage.py migrate

echo "Creating superuser (if managed)"
python3 /scripts/create_superuser.py

echo "Starting Gunicorn"
exec gunicorn sensor.wsgi -t 3600 -c ../gunicorn/config.py &
wait
