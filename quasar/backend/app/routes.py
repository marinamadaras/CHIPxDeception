from flask import Blueprint, current_app, request, jsonify, redirect, Response
from flask_sse import sse
import requests
import os
from datetime import datetime

bp = Blueprint('main', __name__)


@bp.route('/')
def hello():
    print("TEST", flush=True)
    return 'Hello, I am the website backend module!'


@bp.route('/response', methods=['POST'])
def response():
    data = request.json
    sse.publish({'message': data['message']}, type='response')
    return "Message sent!"

# @app.route('/api/v1/<path1>', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH']) @app.route('/api/v1/<path1>/<path2>', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH']) @app.route('/api/v1/<path1>/<path2>/<path3>', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH']) 
@bp.route('/kgraph/<path1>/<path2>/<path3>/<path4>/<path5>/<path6>/<path7>', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@bp.route('/kgraph/<path1>/<path2>/<path3>/<path4>/<path5>/<path6>', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@bp.route('/kgraph/<path1>/<path2>/<path3>/<path4>/<path5>', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@bp.route('/kgraph/<path1>/<path2>/<path3>/<path4>', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@bp.route('/kgraph/<path1>/<path2>/<path3>', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@bp.route('/kgraph/<path1>/<path2>', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@bp.route('/kgraph/<path1>', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@bp.route('/kgraph', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def kgraph(path1='', path2='', path3='', path4='', path5='', path6='', path7=''):
    URL = request.url.replace(request.host_url + 'kgraph', 'http://knowledge:7200')

    res = requests.request(  # ref. https://stackoverflow.com/a/36601467/248616
        method=request.method,
        url=request.url.replace(request.host_url + 'kgraph', 'http://knowledge:7200'),
        # exclude 'host' header
        headers={k: v for k, v in request.headers if k.lower() != 'host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
    )

    print(1, URL, flush=True)
    print(2, request.host_url, flush=True)
    print(3, request.url, flush=True)
    print(4, res.url, flush=True)

    # region exlcude some keys in :res response
    # NOTE we here exclude all "hop-by-hop headers" defined by RFC 2616 section 13.5.1 ref. https://www.rfc-editor.org/rfc/rfc2616#section-13.5.1
    excluded_headers = ['content-encoding',
                        'content-length', 'transfer-encoding', 'connection']

    headers = [
        (k, v) for k, v in res.raw.headers.items()
        if k.lower() not in excluded_headers
    ]
    # endregion exlcude some keys in :res response
    try:
        c = res.content.decode('utf-8')
        c = c.replace('src="', 'src="http://localhost:9000/api/kgraph/')
        c = c.replace('href="', 'href="http://localhost:9000/api/kgraph/')
        c = c.encode()
    except:
        c = res.content
    response = Response(c, res.status_code, headers)

    # print(c, flush=True)

    return response


@bp.route('/submit', methods=['POST'])
def submit():
    data = request.json
    data["timestamp"] = datetime.now().isoformat()  # NOTE: consider moving this to frontend as well

    requests.post(f"http://response-generator:5000/subject-sentence", json=data)
    requests.post(f"http://text-to-triples:5000/new-sentence", json=data)

    return f"Submitted sentence '{data['sentence']}' from {data['patient_name']} to t2t!"
