from flask import Blueprint, current_app, request, jsonify
import requests
import app.util
import os

bp = Blueprint('main', __name__)


@bp.route('/')
def hello():
    return 'Hello, I am the reasoning module!'


@bp.route('/query-knowledge', methods=['POST'])
def query_knowledge():
    return 'OK'


@bp.route('/store-knowledge', methods=['POST'])
def store_knowledge():
    # Get JSON data from the POST request
    current_app.logger.info(f"Triples received: {request.json}")
    json_data = request.json
    triples = json_data['triples']
    sentence_data = json_data['sentence_data']
    result = "Empty triple set received", 200

    if len(triples) > 0:
        current_app.logger.debug(f"triples: {triples}")
        triple = triples[0]
        # Convert JSON triple to RDF data
        rdf_data = app.util.json_triple_to_rdf(triple)
        current_app.logger.debug(f"rdf_data: {rdf_data}")

        # Upload RDF data to GraphDB
        response = app.util.upload_rdf_data(rdf_data)
        if response.status_code == 204:
            result = jsonify({"message": "Data uploaded successfully!"}), 200
        else:
            result = jsonify({"error": f"Failed to upload data: {response.status_code}, {response.text}"}), response.status_code

    # IF DONE, START REASONING (should query knowledge base somehow)
    app.util.reason_and_notify_response_generator(sentence_data)
    return result


# NOTE: By making this a route, it needs to receive the correct input as well.
# This is somewhat bad... It complicates the design. Some questions:
# - Do we even want people ot be able to just call this separately?
# - Does this mean we need state? We need to somehow pass the sentence data to the reasoner
# - I see that we only really use the sentence_data, so we definitely do not need the triples for sending a message to the response gen
# - We DO however need the sentence data, because we can't obtain that from anywhere else. This makes sense.
# - That means we EXPECT a post, with the sentence data itself.

# Note that we first check if we can give advice, and if that is "None",
# then we try to formulate a question instead.
@bp.route('/reason', methods=['POST'])
def reason():
    sentence_data = request.json
    app.util.reason_and_notify_response_generator(sentence_data)
    return 'OK', 200

