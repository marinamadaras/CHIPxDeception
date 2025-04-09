from flask import Flask
from logging.handlers import HTTPHandler
from logging import Filter
from app.util.db import close_db
import os


class ServiceNameFilter(Filter):
    def filter(self, record):
        record.service_name = "Reasoner"
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

    response_generator_address = core_module_address("RESPONSE_GENERATOR_MODULE")
    if response_generator_address:
        flask_app.config["RESPONSE_GENERATOR_ADDRESS"] = response_generator_address

    knowledge_address = os.environ.get("KNOWLEDGE_DEMO", None)
    if knowledge_address:
        repository_name = 'repo-test-1'  # This is temporary
        flask_app.config['knowledge_url'] = f"http://{knowledge_address}/repositories/{repository_name}"
        flask_app.teardown_appcontext(close_db)

    from app.routes import bp
    flask_app.register_blueprint(bp)

    return flask_app
