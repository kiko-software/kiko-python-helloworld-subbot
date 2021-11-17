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

import os
import requests
import json
from flask import Flask, request, abort
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def health():
  return "ping"

@app.route("/api/v1/messages", methods = ['POST'])
def helloworld_subbot():
    kiko_instance_domain = request.args.get('callback-domain')
    if kiko_instance_domain is None:
        abort(400, description = "callback-domain not found")    

    conversation_id = request.get_json().get('conversationId')
    if conversation_id is None:
        abort(400, description = "conversationId not found")
    
    base_url = "https://" + kiko_instance_domain + "/api"    

    r = requests.post(url = base_url + "/api/v1/conversation/send", json={
        "conversationId": conversation_id,
        "messages": [
            {
                "type": "message",
                "data": {
                    "type": "text/plain",
                    "content": "Hello World"
                }
            },
            {
                "type": "event",
                "name": "endOfConversation"
            }
        ] 
    })
    # app.logger.info('request result: %s', r)

    return {"success": True}

@app.errorhandler(HTTPException)
def handle_exception(e):
    # start with the correct headers and status code from the error
    response = e.get_response()

    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
