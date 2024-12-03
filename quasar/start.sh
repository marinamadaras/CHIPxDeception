#!/bin/bash

# Start the backend
cd /backend
gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()' --worker-class gevent --reload &

# Start the frontend - for now use dev server
cd /frontend
quasar dev &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?