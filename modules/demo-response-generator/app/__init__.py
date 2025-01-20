from flask import Flask
from logging.handlers import HTTPHandler
from logging import Filter
import os


class ServiceNameFilter(Filter):
    def filter(self, record):
        record.service_name = "Response Generator"
        return True


def create_app(test=False):
    flask_app = Flask(__name__)

    logger_address = os.environ.get("LOGGER_ADDRESS", None)

    if logger_address and not test:
        http_handler = HTTPHandler(logger_address, "/log", method="POST")
        flask_app.logger.addFilter(ServiceNameFilter())
        flask_app.logger.addHandler(http_handler)

    from app.routes import bp
    flask_app.register_blueprint(bp)

    return flask_app
