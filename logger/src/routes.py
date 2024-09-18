from flask import Blueprint, current_app
from datetime import datetime

bp = Blueprint('main', __name__)


@bp.route('/')
def hello():
    return 'Hello, I am the logger module!'


@bp.route('/log/<line>')
def log(line: str):
    timestamp = datetime.now().isoformat()
    current_app.logger.info(f'{timestamp}:::{line}')

    # with open(Path.home() / 'chip.log', 'a') as f:
    #     f.writelines([f'{timestamp}:::{line}'])
    return f"logged: {line}"
