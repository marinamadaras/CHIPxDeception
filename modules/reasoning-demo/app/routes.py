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
    reason_and_notify_response_generator(json_data)

    return result


# Note that we first check if we can give advice, and if that is "None",
# then we try to formulate a question instead.
@bp.route('/reason')
def reason_and_notify_response_generator(text_to_triple_data):
    payload = app.util.reason()
    payload['sentence_data'] = text_to_triple_data['sentence_data']
    response_generator_address = current_app.config.get("RESPONSE_GENERATOR_ADDRESS", None)
    if response_generator_address:
        requests.post(f"http://{response_generator_address}/submit-reasoner-response", json=payload)

    return 'OK', 200
