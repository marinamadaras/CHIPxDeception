from flask import Blueprint, current_app, request
import app.util

bp = Blueprint('main', __name__)


@bp.route('/submit-reasoner-response', methods=['POST'])
def submit_reasoner_response():
    data = request.json
    current_app.logger.info(f"Received data from reasoner: {data}")
    reasoner_response = data

    app.util.send_message(reasoner_response)

    return 'OK'


@bp.route('/')
def hello():
    return 'Hello, I am the response generator module!'
