from flask import g
from transformers import AutoTokenizer, pipeline, Pipeline, BitsAndBytesConfig
import torch


class LLMExtension:
    pipe: Pipeline


    def __init__(self, app=None, model_name=None):
        if app is not None and model_name is not None:
            self.init_app(app, model_name)


    def init_model(self, model_name):
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        pipe = pipeline("text-generation", model=model_name, tokenizer=model_name, max_new_tokens=500, model_kwargs={"quantization_config": bnb_config, "torch_dtype": torch.float16, "low_cpu_mem_usage": True})
        return pipe


    def init_app(self, app, model_name):
        self.pipe = self.init_model(model_name)
        app.extensions = getattr(app, "extensions", {})
        app.extensions["pipe"] = self.pipe
        # app.before_request(...)
