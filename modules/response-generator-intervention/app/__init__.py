from flask import Flask
from logging.handlers import HTTPHandler
from logging import Filter
from app.util.llm_extension import LLMExtension
from app.framing_strategy.framing_strategy_service import FramingStrategyService
import os

# NOTE: This approach will load the model for every instance of the application.
llm = LLMExtension()
response_framer = FramingStrategyService()

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

    flask_app.config['GEMINI_API_KEY'] = os.environ['GEMINI_API_KEY']
    flask_app.config['FRAMING_STRATEGY'] = os.environ['FRAMING_STRATEGY']

    llm.init_app(flask_app)
    response_framer.init_app(flask_app)

    return flask_app
