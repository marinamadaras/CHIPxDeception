from flask import Flask, request
import requests
import json

app = Flask(__name__)
app.debug = True

# This is the front-end's "back-end" (as silly as that sounds)
# Here we can get input from the other containers

# Since this is the front-end, it is exposed to the host
# Meaning you can just go to "localhost:5000" in your web browser
# And access it. By default, it should show the "hello" sentence below.

# The default route
@app.route('/')
def hello():
    return 'Hello, I am the front end module!'

# Initialize everything - for now just configuring the knowledge base
@app.route('/init')
def init():
    files = {'config': ('config', open('/data/repo-config.ttl', 'rb'))}
    res = requests.post(f'http://knowledge:7200/rest/repositories', files=files)
    if res.status_code in range(200, 300):
        return f"Successfully initialized GraphDB repository (status code {res.status_code})"
    return f"There was potentially a problem with initializing the repository (status code {res.status_code}): {res.text}"

# Can ping the other containers with this
# Type e.g. "localhost:5000/ping/text-to-triples" to say hi to the text-to-triples container
@app.route('/ping/<name>')
def ping(name):
    r = requests.get(f'http://{name}:5000/')
    return r.text

@app.route('/response', methods=['POST'])
def response():
    data = request.json
    print(f"Received a reply! {data}", flush=True)
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
