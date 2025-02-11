from flask import Flask
from logging.handlers import HTTPHandler
from logging import Filter
from app.model_extension import ModelExtension
import os



# NOTE: This approach will load the model for every instance of the application.
model = ModelExtension()

class ServiceNameFilter(Filter):
    def filter(self, record):
        record.service_name = "Text 2 Triple"
        return True


def core_module_address(core_module):
    try:
        return os.environ[os.environ[core_module]]
    except KeyError:
        return None


def create_app(test=False):
    flask_app = Flask(__name__)

    logger_address = os.environ.get("LOGGER_ADDRESS", None)

    if logger_address and not test:
        http_handler = HTTPHandler(logger_address, "/log", method="POST")
        flask_app.logger.addFilter(ServiceNameFilter())
        flask_app.logger.addHandler(http_handler)

    reasoner_address = core_module_address('REASONER_MODULE')
    if reasoner_address:
        flask_app.config['REASONER_ADDRESS'] = reasoner_address

    model.init_app(flask_app)


    from app.routes import bp
    flask_app.register_blueprint(bp)

    return flask_app
