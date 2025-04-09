#!/bin/bash

cd src

# Start the first process
# python app.py &

# Start the second process
# python gradio_app.py &

uvicorn gradio_app:app --host 0.0.0.0

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?