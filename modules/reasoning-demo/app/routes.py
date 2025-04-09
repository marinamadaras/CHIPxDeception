from flask import Blueprint, current_app, request
from contextlib import suppress
import app.util

bp = Blueprint('main', __name__)


@bp.route('/')
def hello():
    return 'Hello, I am the reasoning module!'


@bp.route('/process', methods=['POST'])
def process():
    current_app.logger.info(f"Triples received: {request.json}")
    json_data = request.json
    triples = json_data['triples']
    sentence_data = json_data['sentence_data']

    # Keep the flow going regardless of the storage error.
    with suppress(RuntimeError):
        app.util.store_knowledge(triples)
    app.util.reason_and_notify_response_generator(sentence_data)
    return 'OK', 200


@bp.route('/store', methods=['POST'])
def store():
    json_data = request.json
    triples = json_data['triples']

    try:
        app.util.store_knowledge(triples)
        return 'OK', 200
    except RuntimeError as e:
        return str(e), 500  


@bp.route('/reason', methods=['POST'])
def reason():
    sentence_data = request.json
    app.util.reason_and_notify_response_generator(sentence_data)
    return 'OK', 200

