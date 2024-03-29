#!/bin/bash
# this script is used to boot a Docker container
source venv/bin/activate
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
export FLASK_DEBUG=1
flask translate compile
exec gunicorn -b :8080 --access-logfile - --error-logfile - torqata:app