from unittest.mock import ANY
from flask import Blueprint, current_app, request
import app.util

bp = Blueprint('main', __name__)


@bp.route('/')
def hello():
    return "Hello, I am the text to triples module!"


@bp.route('/new-sentence', methods=['POST'])
def new_sentence():
    sentence_data = request.json
    sentence = sentence_data['sentence']
    patient_name = sentence_data['patient_name']
    timestamp =sentence_data['timestamp']
    current_app.logger.debug(f"Patient {patient_name} wrote {sentence} at {timestamp}")
    app.util.send_triples(sentence_data)
    return 'OK'
