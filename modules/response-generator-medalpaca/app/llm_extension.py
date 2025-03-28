from flask import g
# from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer, pipeline, BitsAndBytesConfig
import torch


class LLMExtension:
    # model = None
    # tokenizer = None
    pipe = None


    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)


    def init_model(self):
        model_name = "medalpaca/medalpaca-7b"
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        # pl = pipeline(\"text-generation\", model=\"medalpaca/medalpaca-7b\", tokenizer=\"medalpaca/medalpaca-7b\",  )
        # model = AutoAWQForCausalLM.from_quantized(model_name, fuse_layers=True, trust_remote_code=False, safetensors=True, offload_folder='/offload')
        # tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=False)
        pipe = pipeline("text-generation", model=model_name, tokenizer=model_name, max_new_tokens=500, model_kwargs={"quantization_config": bnb_config, "torch_dtype": torch.float16, "low_cpu_mem_usage": True})
        return pipe


    def init_app(self, app):
        self.pipe = self.init_model()
        app.extensions = getattr(app, "extensions", {})
        app.extensions["pipe"] = self.pipe
        # app.before_request(...)
