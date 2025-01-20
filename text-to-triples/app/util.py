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

# NOTE: Deprecated, as this way of extracting tuples does not work properly:
#       - Assumes a sentence structure where the patient talks in third person; instead, the subject should always be the patient if the patient uses "I".
#       - Even then, a simple sentence such as "I like eating with my mother" is not captured properly, as it'll become 'sub:I pred:like obj:mother'
def extract_triples(patient_name, sentence):
    triples = []
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


def send_triples(patient_name, sentence):
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

    payload = extract_triples(patient_name, sentence)
    payload["patient_name"] = patient_name
    current_app.logger.debug(f"payload: {payload}")
    reasoning_address = os.environ.get('REASONING_ADDRESS', None)
    if reasoning_address:
        requests.post(f"http://{reasoning_address}/store-knowledge", json=payload)