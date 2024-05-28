from flask import Flask, request
import requests
import json
from dataclasses import dataclass

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')



app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return 'Hello, I am the text to triples module!'

@app.route('/new-sentence', methods=['POST'])
def new_sentence():
    data = request.json
    sentence = data["sentence"]
    patient_name = data['patient_name']
    print(f"Patient {patient_name} wrote {sentence}", flush=True)
    send_triples(patient_name, sentence)
    return 'OK'

def create_triple(subj, pred, obj):
    return {"subject":subj, "object":obj, "predicate":pred}

def infer_triples(patient_name, sentence):
    # Do something to infer triples here...
    # For now, a hard-coded response
    return [
        create_triple("Julia", "hasValue", "Family"),
        create_triple("Julia", "hasPreference", "NoMedication")
    ]

def extract_triples(patient_name, sentence):
    triples = []
    tokens = word_tokenize(sentence)
    tagged_tokens = pos_tag(tokens)

    subject = patient_name  
    predicate = None
    object_ = None
    for word, tag in tagged_tokens:
        if tag.startswith('VB') and predicate is None:
            predicate = word
        elif tag.startswith(('NN', 'NNS', 'NNP', 'NNPS')) and predicate and subject and object_ is None:
            object_ = word
            break

    if subject and predicate and object_:
        triple_dict = {"subject": subject, "object": object_, "predicate": predicate}
        triples.append(triple_dict)

    return {"triples": triples}

def send_triples(patient_name, sentence):
    payload = extract_triples(patient_name, sentence)
    requests.post("http://reasoning:5000/store-knowledge", json=payload)
    print(payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
