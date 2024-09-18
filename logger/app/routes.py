from flask import Blueprint, current_app
from datetime import datetime
from logging import FileHandler

bp = Blueprint('main', __name__)


@bp.route('/')
def hello():
    return 'Hello, I am the logger module!'


@bp.route('/log/<line>')
def log(line: str):
    timestamp = datetime.now().isoformat()
    current_app.logger.info(f'{timestamp}:::{line}')
    return f"logged: {line}"


@bp.route('/log')
def get_log():
    for handler in current_app.logger.handlers:
        if isinstance(handler, FileHandler) and 'chip' in handler.baseFilename:
            with open(handler.baseFilename, 'r') as f:
                return f.readlines()
    return "No log file found!", 503
