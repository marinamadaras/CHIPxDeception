from flask import g
# from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer, pipeline



class LLMExtension:
    # model = None
    # tokenizer = None
    pipe = None


    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)


    def init_model(self):
        model_name = "medalpaca/medalpaca-7b"
        # model = AutoAWQForCausalLM.from_quantized(model_name, fuse_layers=True, trust_remote_code=False, safetensors=True, offload_folder='/offload')
        # tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=False)
        pipe = pipeline("text-generation", model=model_name, tokenizer=model_name, max_new_tokens=500)
        return pipe


    def init_app(self, app):
        self.pipe = self.init_model()
        app.extensions = getattr(app, "extensions", {})
        app.extensions["pipe"] = self.pipe
        # app.before_request(...)
