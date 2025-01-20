from flask import Blueprint, current_app, request
from logging import FileHandler

bp = Blueprint('main', __name__)


@bp.route('/')
def hello():
    return 'Hello, I am the logger module!'


@bp.route('/log/<line>', methods=['GET'])
def log(line: str):
    current_app.logger.info(line)
    return f"logged: {line}"


@bp.route('/log', methods=['GET'])
def get_log():
    for handler in current_app.logger.handlers:
        if isinstance(handler, FileHandler) and 'chip' in handler.baseFilename:
            with open(handler.baseFilename, 'r') as f:
                return f.readlines()
    return "No log file found!", 503


@bp.route('/log', methods=['POST'])
def log_post():
    line = request.form["msg"]
    service = request.form["service_name"]
    level = int(request.form["levelno"])
    current_app.logger.log(level, f"{service} ::: {line}")
    return f"logged: {line}"
