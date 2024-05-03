FROM python:3-slim

# Install python deps
COPY requirements.txt /
RUN pip3 install -r /requirements.txt

# Copy over source
COPY src /src

# Run the server
WORKDIR src
CMD [ "python", "app.py" ]