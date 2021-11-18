"""processes the user input messages from metabot"""

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from datetime import datetime
from flask import Flask, request, abort
from flask.logging import create_logger
from werkzeug.exceptions import HTTPException
from google.cloud import firestore
import requests

app = Flask(__name__)
app.logger = create_logger(app)
db = firestore.Client()
kiko_instances = db.collection('kiko-instances')

# ---
end_of_conversation_message = {
    "type": "event",
    "name": "endOfConversation"
}


@app.route("/", methods=['GET'])
def health():
    """only for health checks"""
    return "ping"


@app.route("/api/v1/messages", methods=['POST'])
def api_v1_messages_post():
    """processes the user input messages from metabot"""

    # init --------------------------

    # i.e. "cloud02-7c83ec0.prod.1000grad.de" - this value is to be added to
    # the webhook-url as a parameter
    kiko_instance_identifier = request.args.get('callback-domain')
    if kiko_instance_identifier is None:
        abort(400, description="callback-domain not found")

    # the source of this value is a webhook -
    # https://cloud02-7c83ec0.prod.1000grad.de/api/docs/#/webhooks?id=message_sent
    body = request.get_json()
    conversation_id = body.get('conversationId')
    if conversation_id is None:
        abort(400, description="conversationId not found")
    # app.logger.info('---------------- conversation_id: %s', conversation_id )

    messages = body.get('messages')

    metadata = messages[0].get("metaData")

    # The cms sends each new user message to the subbot. however, the metadata from the intent
    # is still contained in the first message. This is why the metadata is
    # stored in a conversation-db.
    conversation = upsert_conversation_data(
        kiko_instance_identifier, conversation_id, metadata)
    if conversation is None:
        abort(400, description="Missing conversation item")

    is_first_request = False
    if metadata is not None:
        is_first_request = True
        metadata = conversation["metadata"]

    base_api_url = "https://" + kiko_instance_identifier + "/api"
    send_url = base_api_url + "/api/v1/conversation/send"

    # validate input from cms --------------------------------

    if is_first_request:
        # ask user for the name

        parameters = metadata["parameters"]
        if parameters is None:
            abort(400, description="Missing parameters in the intent metadata")

        parameter_question = parameters[0]["question"]
        if parameter_question is None:
            abort(
                400,
                description="Missing question in the first parameter of the intent metadata")

        parameter_name = parameters[0]["name"]
        if parameter_name is None:
            abort(
                400,
                description="Missing name in the first parameter of the intent metadata")

        # update session with the parameter name
        upsert_conversation_data(
            kiko_instance_identifier,
            conversation_id,
            last_input_parameter_identifier=parameter_name)

        requests.post(url=send_url, json={
            "conversationId": conversation_id,
            "messages": [
                {
                    "type": "message",
                    "data": {
                        "type": "text/plain",
                        "content": parameter_question
                    }
                }
            ]
        })
    else:
        # user input data are in "messages" - this should be the answer
        # of the last question from the bot
        # app.logger.info('---------------- messages: %s', messages )
        if (len(messages) == 1 and messages[0]["type"] == 'message'):
            input_data = messages[0]["data"]
            if input_data["type"] == 'text/plain':
                input_data_content = input_data["content"]

                # proccess --------------------------------
                # app.logger.info('---------------- conversation: %s', conversation )
                input_parameter_identifier = conversation["last_input_parameter_identifier"]
                if input_parameter_identifier is None:
                    abort(
                        400, description="Missing input_parameter_identifier in the conversation")

                app.logger.info('input_parameter_identifier: %s',
                                input_parameter_identifier)
                app.logger.info('input_data_content: %s', input_data_content)

                user_name = input_data_content
                requests.post(url=send_url, json={
                    "conversationId": conversation_id,
                    "messages": [
                        {
                            "type": "message",
                            "data": {
                                "type": "text/plain",
                                "content": "Hallo " + user_name
                            }
                        }, end_of_conversation_message
                    ]
                })
    return {"success": True}


@app.errorhandler(HTTPException)
def handle_exception(err):
    """for better error handling"""
    # start with the correct headers and status code from the error
    response = err.get_response()

    # replace the body with JSON
    response.data = json.dumps({
        "code": err.code,
        "name": err.name,
        "description": err.description,
    })
    response.content_type = "application/json"
    return response


def upsert_conversation_data(
        kiko_instance_identifier,
        conversation_id,
        metadata=None,
        last_input_parameter_identifier=None):
    """ Looks up (or creates) the session with the given conversation_session_id.
    """
    kiko_conversations = kiko_instances.document(
        kiko_instance_identifier).collection('kiko-conversations')
    doc_ref = kiko_conversations.document(document_id=conversation_id)
    doc = doc_ref.get()
    if doc.exists:
        kiko_conversation = doc.to_dict()
    else:
        kiko_conversation = {
            "created": datetime.now(tz=None),
            "metadata": metadata  # save metadata only at first time
        }
    if last_input_parameter_identifier is not None:
        kiko_conversation["last_input_parameter_identifier"] = last_input_parameter_identifier

    doc_ref.set(kiko_conversation, merge=True)
    return kiko_conversation
