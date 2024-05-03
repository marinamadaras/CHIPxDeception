from flask import Flask
import requests
import json
from datetime import datetime

app = Flask(__name__)
app.debug = True

log = []

@app.route('/')
def hello():
    return 'Hello, I am the logger module!'

@app.route('/log/<line>')
def log(line):
    timestamp = datetime.datetime.now().isoformat()
    log.append({"timestamp": timestamp, "content": line})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
