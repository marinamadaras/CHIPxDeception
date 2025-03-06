FROM python:3.11-slim

# Install python deps: 
# - Torch needs to be pre-installed for autoawq
# - The order of operations is done such that changing the requirements won't require reinstalling Torch or the model from scratch
# RUN pip3 install torch==2.5.1 intel-extension-for-pytorch==2.5.0
# RUN pip3 install autoawq==0.2.8
# RUN pip3 install transformers tiktoken protobuf blobfile

RUN pip3 install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install transformers protobuf tiktoken blobfile sentencepiece
RUN python3 -c "from transformers import pipeline; pl = pipeline(\"text-generation\", model=\"medalpaca/medalpaca-7b\", tokenizer=\"medalpaca/medalpaca-7b\"); pl(\"some input\")"
COPY requirements.txt /
RUN pip3 install -r /requirements.txt
RUN apt-get update && apt-get install -y curl \
libzmq3-dev \
build-essential \
g++ \
libsm6 \
libxext6 \
libxrender-dev \
libgl1


# Copy over source
COPY app /app

# Run the server
CMD [ "flask", "--app", "app", "--debug", "run", "--host", "0.0.0.0"]

