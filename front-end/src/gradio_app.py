from fastapi import FastAPI, Request
import gradio as gr
import requests
import datetime
import time

CUSTOM_PATH = "/gradio"

app = FastAPI()


@app.get("/")
def read_main():
    return {"message": "Welcome to the CHIP demo!"}


@app.post("/response")
async def response(request: Request):
    data = await request.json()
    print("Got a response", data, flush=True)
    global resp
    resp = data["reply"]
    return {"message": "OK!"}


# Initialize everything - for now just configuring the knowledge base
@app.get('/init')
def init():
    files = {'config': ('config', open('/data/repo-config.ttl', 'rb'))}
    res = requests.post(f'http://knowledge:7200/rest/repositories', files=files)
    if res.status_code in range(200, 300):
        return f"Successfully initialized GraphDB repository (status code {res.status_code})"
    return f"There was potentially a problem with initializing the repository (status code {res.status_code}): {res.text}"


@app.get('/ping/{name}')
def ping(name: str):
    r = requests.get(f'http://{name}:5000/')
    return r.text

# For now used to wait for a response
# Will be set by the response generator via the /response route
resp = None


# I suspect that gradio only sends the sentence text to the method
# So for all intents and purposes we can just generate a timestamp
# And fix the patient's name. If we can somehow store the patient's
# name, then we should use that of course.
def send_to_t2t(chat_message):
    payload = {
        "patient_name": "Julia",
        "sentence": chat_message,
        "timestamp": datetime.datetime.now().isoformat()
    }
    requests.post(f"http://response-generator:5000/subject-sentence", json=payload)
    requests.post(f"http://text-to-triples:5000/new-sentence", json=payload)

    # This will definitely change, but is good enough for the demo
    # I just haven't found a way yet to make gradio update its UI from an
    # API call...
    global resp
    reply = resp
    while True:
        time.sleep(0.2)
        if resp is not None:
            reply = resp
            resp = None
            break

    return reply


io = gr.Interface(fn=send_to_t2t, inputs="textbox", outputs="textbox")
gradio_app = gr.routes.App.create_app(io)
app.mount(CUSTOM_PATH, gradio_app)