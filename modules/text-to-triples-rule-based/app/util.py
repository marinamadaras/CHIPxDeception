from flask import current_app
import nltk
import requests
import os


def postprocess_triple(triple, userID):
    subject, predicate, object_ = triple['subject'], triple['predicate'], triple['object']
    if subject == 'relationships':
        subject = 'warm_relationships'
    if object_ == 'relationships':
        object_ = 'warm_relationships'

    if predicate == "prioritize":
        predicate = "prioritizedOver"
        subject = f"{userID}_{subject}"
        object_ = f"{userID}_{object_}"

    if subject == "habit" and predicate == "have":
        subject = userID
        predicate = "hasPhysicalActivityHabit"
        object_ = f"activity_{object_}"

    return {
        'subject': subject,
        'predicate': predicate,
        'object': object_,
    }


def extract_triples(sentence_data):
    triples = []
    patient_name = sentence_data['patient_name']
    sentence = sentence_data['sentence']
    tokens = nltk.word_tokenize(sentence)
    tagged_tokens = nltk.pos_tag(tokens)

    predicate = None
    object_ = None
    subject= None
    current_app.logger.debug(f"tagged tokens: {tagged_tokens}")

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


def send_triples(sentence_data):
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

    payload = extract_triples(sentence_data)
    payload['sentence_data'] = sentence_data
    current_app.logger.debug(f"payload: {payload}")
    reasoner_address = current_app.config.get('REASONER_ADDRESS', None)
    if reasoner_address:
        requests.post(f"http://{reasoner_address}/process", json=payload)