This is a simple tech review application to search and add movies to a database

gcloud builds submit --tag gcr.io// --project=

gcloud run deploy --image gcr.io// --platform managed --project= --allow-unauthenticated --region us-east1

gcloud iam service-accounts list --project=

gcloud iam service-accounts keys create ./keys.json --iam-account email@address

gcloud auth activate-service-account --key-file=keys.json

docker build -t torqata:latest .
docker run --name torqata -d -p 8000:5000 --rm torqata:latest

conda activate torqata
set FLASK_APP=torqata.py
set FLASK_CONFIG=config.py
set FLASK_DEBUG=1
flask run
