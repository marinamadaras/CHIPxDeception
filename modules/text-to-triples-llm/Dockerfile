FROM python:3.10-slim

# Install python deps
COPY requirements.txt /
RUN pip3 install -r /requirements.txt
RUN apt-get update
RUN apt-get install -y curl 

RUN curl --create-dirs -LO --output-dir / https://huggingface.co/StergiosNt/spo_labeling_bert/resolve/main/best_model.pth

# Copy over source
COPY app /app

# Run the server
CMD [ "flask", "--app", "app", "--debug", "run", "--host", "0.0.0.0"]
