from flask import Blueprint, current_app, request, jsonify, redirect, Response
import flask_sse
import requests
import os
from datetime import datetime

bp = Blueprint('main', __name__)


@bp.route('/')
def hello():
    return 'Hello, I am the website backend module!'


@bp.route('/response', methods=['POST'])
def response():
    data = request.json
    flask_sse.sse.publish({'message': data['message']}, type='response')
    return "Message sent!"


@bp.route('/submit', methods=['POST'])
def submit():
    data = request.json

    resgen_address = current_app.config.get("RESPONSE_GENERATOR_ADDRESS", None)
    if resgen_address:
        requests.post(f"http://{resgen_address}/subject-sentence", json=data)
    
    t2t_address = current_app.config.get("TRIPLE_EXTRACTOR_ADDRESS", None)
    if t2t_address:
        requests.post(f"http://{t2t_address}/new-sentence", json=data)

    return f"Submitted sentence '{data['sentence']}' from {data['patient_name']} to t2t!"
