from flask import g
import torch



class ModelExtension:
    model = None


    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)


    def init_model(self):
        model_path = r'/best_model.pth'
        model = torch.load(model_path)

        # Switch the model to evaluation mode
        model.eval()
        return model


    def get_model(self):
        return self.model


    def init_app(self, app):
        self.model = self.init_model()
        app.extensions = getattr(app, "extensions", {})
        app.extensions["model"] = self.model
        # app.before_request(...)
