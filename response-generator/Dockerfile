FROM python:3-slim

# Install python deps
COPY requirements.txt /
COPY src /src
RUN pip3 install -r /requirements.txt

# Run the server
WORKDIR src
CMD [ "python", "app.py" ]