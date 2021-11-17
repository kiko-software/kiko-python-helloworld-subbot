# Kiko Hello World Subbot Sample with Python

This sample shows how to deploy a Kiko Hello World subbot application.

## Build

```
docker build --tag kiko-python-helloworld-subbot:python .
```

## Run Locally

```
docker run --rm -p 9090:8080 -e PORT=8080 kiko-python-helloworld-subbot:python
```

## Deploy

```sh
# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/kiko-python-helloworld-subbot

# Deploy to Cloud Run
gcloud run deploy kiko-python-helloworld-subbot \
--image gcr.io/${GOOGLE_CLOUD_PROJECT}/kiko-python-helloworld-subbot
```
