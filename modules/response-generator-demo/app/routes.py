from flask import Blueprint, current_app, request
import app.util

bp = Blueprint('main', __name__)


@bp.route('/subject-sentence', methods=['POST'])
def submit_sentence():
    data = request.json
    current_app.logger.info(f"Received sentence: {data}")
    app.util.sentence_data = data

    app.util.check_responses()

    return 'OK'


@bp.route('/submit-reasoner-response', methods=['POST'])
def submit_reasoner_response():
    data = request.json
    current_app.logger.info(f"Received data from reasoner: {data}")
    app.util.reasoner_response = data

    app.util.check_responses()

    return 'OK'


@bp.route('/')
def hello():
    return 'Hello, I am the response generator module!'
