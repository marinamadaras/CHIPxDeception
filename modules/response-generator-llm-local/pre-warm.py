import transformers
import sys

def deco(func):
    def _(*args, **kwargs):
        func(*args, **kwargs)
        print("Exiting after downloading models!")
        exit(0)
    return _

transformers.modeling_utils._get_resolved_checkpoint_files = deco(transformers.modeling_utils._get_resolved_checkpoint_files)
model = transformers.AutoModel.from_pretrained(sys.argv[1])