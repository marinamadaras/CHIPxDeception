FROM python:3.10-slim

# Install python deps
COPY requirements.txt /
RUN pip3 install -r /requirements.txt

# Copy source and data files
COPY src /src
COPY data /data

# Copy and chmod start script
COPY start.sh /
RUN chmod a+x start.sh

# Configure Gradio
ENV no_proxy="localhost,127.0.0.1"
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV COMMANDLINE_ARGS="--no-gradio-queue"
# ENV GRADIO_ROOT_PATH="0.0.0.0/gradio"
# Run the server
CMD [ "/start.sh" ]