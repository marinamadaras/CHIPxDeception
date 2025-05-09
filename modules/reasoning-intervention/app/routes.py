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

    #TODO: deal with triples being in this format and not random input, 
    #make mapping between input and data that i will generate later
    #maybe take into accound the knowledge base - this conversion will probably be done here, as it's useless to use the text-2-triples

    # triples = json_data['triples']
    sentence_data = json_data['sentence_data']

    app.util.reason_and_notify_response_generator(sentence_data)
    return 'OK', 200

@bp.route('/reason', methods=['POST'])
def reason():
    sentence_data = request.json
    app.util.reason_and_notify_response_generator(sentence_data)
    return 'OK', 200

