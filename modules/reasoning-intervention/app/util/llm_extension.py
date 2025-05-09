from flask import g
from google import genai

class LLMExtension:
    client: genai.Client | None = None


    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)


    def init_model(self, app):
        gemini_api_key = app.config.get("GEMINI_API_KEY", None)
        client = genai.Client(api_key=gemini_api_key)

        return client


    def init_app(self, app):
        self.client = self.init_model(app)
        app.extensions = getattr(app, "extensions", {})
        app.extensions["client"] = self.client
        # app.before_request(...)