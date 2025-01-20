from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import gradio as gr
import requests
import datetime
import time

CUSTOM_PATH = "/gradio"

app = FastAPI()

# For now used to wait for a response
# Will be set by the response generator via the /response route
resp = None


# NOTE: This is great for debugging, but we shouldn't do this in production...
@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content=jsonable_encoder({"code": 500, "msg": repr(exc)}))

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

@app.get('/ping/{name}')
def ping(name: str):
    r = requests.get(f'http://{name}:5000/')
    return r.text

@app.get('/ping/{name}/{endpoint}')
def ping_endpoint(name: str, endpoint: str):
    r = requests.get(f'http://{name}:5000/{endpoint}')
    return r.text

# I suspect that gradio only sends the sentence text to the method
# So for all intents and purposes we can just generate a timestamp
# And fix the patient's name. If we can somehow store the patient's
# name, then we should use that of course.
def send_to_t2t(chat_message):
    payload = {
        "patient_name": "John",
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
            print(reply, flush=True)
            resp = None
            break

    print("Returning reply:", resp)
    return reply


io = gr.Interface(fn=send_to_t2t, inputs="textbox", outputs="textbox")
gradio_app = gr.routes.App.create_app(io)
app.mount(CUSTOM_PATH, gradio_app)