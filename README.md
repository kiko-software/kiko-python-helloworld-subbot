# Kiko Hello World Subbot Sample With Python

This sample shows how to deploy a Kiko hello world subbot application.

## Introduction
With the Kiko software you can create your own chatbot - https://www.kiko.bot 

Some chatbot responses require external data sources. Kiko forwards such a user request to a so-called external subbot. 
The external subbot is an individual web service that fetches the required data e.g. from an external data source and then sends the response text back to the Kiko server. From there, the answer is sent to the user's chat.

Here we show an example web service based on python. 
The web service can be hosted at e.g. Google Cloud Run.

## Look at the code
The processing of the request from the Kiko server takes place in the file main.py.

The response content is in this example is a simple "Hello World" text.

To answer the intent, a server request is sent to Kiko.
The destination address is determined from the callback-domain url parameter of the subbot request.
To ensure that the answer appears in the correct chat with the requesting user, the ConversationId from the request must be used in the answer.
The last message item is an event that ends the conversation with the subbot.

## Setup Local Python Environment

Create and setup virtual environment
```
python -m venv env
source env/bin/activate
env/bin/pip install -U pip
env/bin/pip install -r requirements.txt
```

##  Run the Server Locally 

Activate the virtual environment, if necessary
```
source env/bin/activate
```

Run
```
FLASK_APP=main flask run
```
Check it out: http://127.0.0.1:5000/

## Expose your local service to the world

Open a new terminal and install nodejs, npm and localtunnel e.g. on macOS
```
brew install node
npm install -g localtunnel
```

Expose your local service port to your individual public https subdomain e.g. yourownprefix-kiko-python-helloworld-subbot
```
lt --port 5000 --subdomain tgd-kiko-python-helloworld-subbot
```
Check it out and press "Click To Continue": https://yourownprefix-kiko-python-helloworld-subbot.loca.lt/

## Webhook Url
You can use this url as endpoint for your webhook - see also https://cloud02-7c83ec0.prod.1000grad.de/api/docs/#/webhooks?id=message_sent

Example webhook url: https://yourownprefix-kiko-python-helloworld-subbot.loca.lt/api/v1/messages?callback-domain=cloud02-7c83ec0.prod.1000grad.de

## Initialize the Deployment With GCP

Create a Google Cloud Platform account https://cloud.google.com/
See: https://console.cloud.google.com/billing

Install the gcloud cli e.g. on macOS
```
brew cask install google-cloud-sdk
```

Initialize the project and config the region
```
gcloud init
gcloud config set run/region europe-west3
```
## Test Drive the Deployment Locally With GCP Buildpacks & Docker

Install pack CLI e.g. on macOS
```
brew install buildpacks/tap/pack
```

Start docker e.g. on macOS
```
open /Applications/Docker.app
```

Build and run locally with Google Cloud Run Buildpacks & Docker
```
pack build --builder=gcr.io/buildpacks/builder kiko-python-helloworld-subbot
docker run -it -ePORT=5000 -p8080:5000 kiko-python-helloworld-subbot
```
Check it out: http://0.0.0.0:8080/

## Deploy and Run on GCP

Set an environment variable with your GCP Project ID
```
gcloud run deploy kiko-python-helloworld-subbot --source .
```
Check out the ping health message: https://kiko-python-helloworld-subbot-.....a.run.app
