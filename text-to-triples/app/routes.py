from flask import Blueprint, current_app, request
import app.util


bp = Blueprint('main', __name__)


@bp.route('/')
def hello():
    return 'Hello, I am the text to triples module!'


@bp.route('/new-sentence', methods=['POST'])
def new_sentence():
    data = request.json
    sentence = data["sentence"]
    patient_name = data['patient_name']
    current_app.logger.debug(f"Patient {patient_name} wrote {sentence}")
    app.util.send_triples(patient_name, sentence)
    return 'OK'
