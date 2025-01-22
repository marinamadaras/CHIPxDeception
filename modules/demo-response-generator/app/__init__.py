from flask import Flask
from logging.handlers import HTTPHandler
from logging import Filter
import os


class ServiceNameFilter(Filter):
    def filter(self, record):
        record.service_name = "Response Generator"
        return True

def core_module_address(core_module):
    try:
        return os.environ[os.environ[core_module]]
    except KeyError:
        return None

def create_app(test=False):
    flask_app = Flask(__name__)

    logger_address = core_module_address("LOGGER_MODULE")
    if logger_address and not test:
        http_handler = HTTPHandler(logger_address, "/log", method="POST")
        flask_app.logger.addFilter(ServiceNameFilter())
        flask_app.logger.addHandler(http_handler)

    frontend_address = core_module_address("FRONTEND_MODULE")
    if frontend_address:
        flask_app.config["FRONTEND_ADDRESS"] = frontend_address

    from app.routes import bp
    flask_app.register_blueprint(bp)

    return flask_app
