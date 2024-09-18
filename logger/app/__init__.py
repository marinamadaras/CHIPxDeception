from flask import Flask


def create_app():
    flask_app = Flask(__name__)

    flask_app.config.update({
        "debug": True,
    })

    from app.routes import bp
    flask_app.register_blueprint(bp)

    return flask_app
