from flask import Flask
from pathlib import Path
from datetime import datetime
from logging import FileHandler, Formatter


def create_app(test=False):
    flask_app = Flask(__name__)
    if test:
        flask_app.logger.handlers = []  # For some reason the handlers persist in pytest fixtures even though the app does not.
    date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    formatter = Formatter("{asctime} - {levelname:<7} - {message}", style="{")

    path = Path('logs') / ('chip-test.log' if test else f'chip-{date}.log')
    file_handler = FileHandler(path, mode='w')
    file_handler.setFormatter(formatter)
    flask_app.logger.addHandler(file_handler)

    from app.routes import bp
    flask_app.register_blueprint(bp)

    return flask_app
