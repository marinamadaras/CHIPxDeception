from flask import Blueprint, current_app, request
import flask_sse
import requests


bp = Blueprint('main', __name__)


@bp.route('/')
def hello():
    return 'Hello, I am the website backend module!'


@bp.route('/process', methods=['POST'])
def response():
    data = request.json
    flask_sse.sse.publish({'message': data['message']}, type='response')
    return "Message sent!"


@bp.route('/submit', methods=['POST'])
def submit():
    data = request.json
    
    t2t_address = current_app.config.get("TRIPLE_EXTRACTOR_ADDRESS", None)
    if t2t_address:
        requests.post(f"http://{t2t_address}/process", json=data)

    return f"Submitted sentence '{data['sentence']}' from {data['patient_name']} to t2t!"
