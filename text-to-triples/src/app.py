from flask import Flask, request
import requests

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
        create_triple("John", "hasValue", "Family"),
        create_triple("John", "hasPreference", "NoMedication")
    ]

def postprocess_triple(triple, userID):
    subject, predicate, object = triple['subject'], triple['predicate'], triple['object']
    if subject == 'relationships':
        subject = 'warm_relationships'
    if object == 'relationships':
        object = 'warm_relationships'

    if predicate == "prioritize":
        predicate = "prioritizedOver"
        subject = f"{userID}_{subject}"
        object = f"{userID}_{object}"
    
    if subject == "habit" and predicate == "have":
        subject = userID
        predicate = "hasPhysicalActivityHabit"
        object = f"activity_{object}"

    return {
        'subject': subject,
        'predicate': predicate,
        'object': object,
    }

def extract_triples(patient_name, sentence):
    triples = []
    tokens = word_tokenize(sentence)
    tagged_tokens = pos_tag(tokens)
    
    predicate = None
    object_ = None
    subject= None
    print('tagged tokens:', tagged_tokens, flush=True)
    for word, tag in tagged_tokens:
        if tag.startswith('VB') and predicate is None:
            predicate = word
        elif tag.startswith(('NN', 'NNS', 'NNP', 'NNPS')) and predicate:
            if subject:
                object_ = word
            else:
                subject = word
    if subject is None:
        subject = patient_name
    if subject and predicate and object_:
        triple_dict = {"subject": subject, "object": object_, "predicate": predicate}
        triples.append(postprocess_triple(triple_dict, patient_name))

    return {"triples": triples}

def send_triples(patient_name, sentence):
    payload = extract_triples(patient_name, sentence)
    print(payload, flush=True)
    requests.post("http://reasoning:5000/store-knowledge", json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
