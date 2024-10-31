from flask import Flask
from logging.handlers import HTTPHandler
from logging import Filter
from app.db import close_db
import os


class ServiceNameFilter(Filter):
    def filter(self, record):
        record.service_name = "Reasoner"
        return True


def create_app(test=False):
    flask_app = Flask(__name__)

    logger_address = os.environ.get("LOGGER_ADDRESS", None)
    if logger_address and not test:
        http_handler = HTTPHandler(logger_address, "/log", method="POST")
        flask_app.logger.addFilter(ServiceNameFilter())
        flask_app.logger.addHandler(http_handler)

    knowledge_address = os.environ.get("KNOWLEDGE_ADDRESS", None)
    if knowledge_address:
        repository_name = 'repo-test-1'  # This is temporary
        flask_app.config['knowledge_url'] = f"http://{knowledge_address}/repositories/{repository_name}"
        flask_app.teardown_appcontext(close_db)

    from app.routes import bp
    flask_app.register_blueprint(bp)

    return flask_app
