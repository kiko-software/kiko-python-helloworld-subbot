# Kiko Hello World Subbot Sample with Python

This sample shows how to deploy a Kiko Hello World subbot application.

[![Run in Google Cloud][run_img]][run_link]

[run_img]: https://storage.googleapis.com/cloudrun/button.svg
[run_link]: https://console.cloud.google.com/cloudshell/editor?shellonly=true&cloudshell_image=gcr.io/cloudrun/button&cloudshell_git_repo=https://github.com/kiko-software/kiko-python-helloworld-subbot&cloudshell_working_dir=run/kiko-python-helloworld-subbot

## Build

```
docker build --tag kiko-python-helloworld-subbot:python .
```

## Run Locally

```
docker run --rm -p 9090:8080 -e PORT=8080 kiko-python-helloworld-subbot:python
```

## Test

```
pytest
```

_Note: you may need to install `pytest` using `pip install pytest`._

## Deploy

```sh
# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/kiko-python-helloworld-subbot

# Deploy to Cloud Run
gcloud run deploy helloworld \
--image gcr.io/${GOOGLE_CLOUD_PROJECT}/kiko-python-helloworld-subbot
```


For more details on how to work with this sample read the [Python Cloud Run Samples README](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/run)
