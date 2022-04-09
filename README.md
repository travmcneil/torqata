This is a simple tech review application to search and add movies to a database

docker build -t torqata:latest .
docker run --name torqata -d -p 8000:5000 --rm torqata:latest

conda activate torqata
set FLASK_APP=torqata.py
set FLASK_CONFIG=config.py
set FLASK_DEBUG=1
flask run
