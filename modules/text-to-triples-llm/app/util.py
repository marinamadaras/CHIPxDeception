import requests
import os

from flask import current_app
from app.t2t_bert import process_input_output
from typing import Dict, Any


def send_triples(data: Dict[str, str]):
    payload = process_input_output(data)
    payload['sentence_data'] = data
    current_app.logger.debug(f"payload: {payload}")
    reasoner_address = current_app.config.get('REASONER_ADDRESS', None)
    if reasoner_address:
        requests.post(f"http://{reasoner_address}/store-knowledge", json=payload)