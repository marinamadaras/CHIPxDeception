import pytest
import logging
from app import create_app
from pathlib import Path
from logging import FileHandler


@pytest.fixture(scope='function')
def app():
    app = create_app(test=True)
    app.config.update({
        "TESTING": True,
    })

    app.logger.setLevel(logging.INFO)  # Needed to ensure that logging can be tested in pytest.

    yield app

    # clean up / reset resources here
    for handler in app.logger.handlers:
        if isinstance(handler, FileHandler) and 'chip' in handler.baseFilename:
            handler.close()
            Path(handler.baseFilename).unlink()


@pytest.fixture()
def client(app):
    return app.test_client()
