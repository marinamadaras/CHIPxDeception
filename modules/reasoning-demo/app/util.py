from rdflib import Graph, Namespace, URIRef, Literal
from app.reason_question import reason_question
from app.reason_advice import reason_advice
from flask import current_app

import requests


# Function to convert a JSON triple to RDF format
def json_triple_to_rdf(triple):
    # Define namespaces
    user_kg = Namespace("http://www.semanticweb.org/aledpro/ontologies/2024/2/userKG#")

    # Create an RDF graph
    g = Graph()
    g.bind("userKG", user_kg)

    # Extract subject, predicate, and object from the JSON data
    subject = triple.get("subject")
    predicate = triple.get("predicate")
    obj = triple.get("object")
    current_app.logger.debug(f"triple: sub:{subject}, pred:{predicate}, obj:{obj}")

    # Construct subject, predicate, and object URIs
    subject_uri = user_kg[URIRef(subject.replace(" ", ""))]
    predicate_uri = user_kg[URIRef(predicate)]
    if isinstance(obj, (int, float)):
        object_uri = Literal(obj)
    else:
        object_uri = user_kg[URIRef(obj.replace(" ", ""))]

    # Add the triple to the graph
    g.add((subject_uri, predicate_uri, object_uri))

    # Serialize the graph to Turtle format and return
    return g.serialize(format="turtle")


# Function to upload RDF data to GraphDB
def upload_rdf_data(rdf_data, content_type='application/x-turtle'):
    """
    Upload RDF data to a GraphDB repository using the REST API.

    :param rdf_data: RDF data in string format (Turtle, RDF/XML, etc.)
    :param content_type: MIME type of the RDF data (default is Turtle)
    :return: Response object
    """
    url = current_app.config.get('knowledge_url', None)
    if not url:
        current_app.logger.warning("No URL configured for knowledge DB, not uploading anything...")
        return


    # Send a POST request to upload the RDF data
    endpoint = f"{url}/statements"
    headers = {
        'Content-Type': content_type
    }
    response = requests.post(endpoint, data=rdf_data, headers=headers)

    if response.ok:
        current_app.logger.info('Successfully uploaded RDF data.')
    else:
        current_app.logger.error(f"Failed to upload data: {response.status_code}, {response.text}")
        raise RuntimeError(f"Could not store data in knowledge base (status: {response.status_code}, {response.text})")


def reason():
    # TODO: Fix the naming inconsistency of the patient
    #     - Use full name in front-end
    #     - Distinguish between first and last name
    #     - Let bot reply with first name
    #     - Store nodes with full name in userKG - or don't use the name at all in the node's identifier
    response = reason_advice("John Mitchel")
    current_app.logger.info(f"advice response: {response}")

    reason_type = 'A'
    if (not response or not response['data']):
        current_app.logger.info("Could not give advice, asking question instead")
        reason_type = 'Q'
        response = reason_question("John")

    # SEND REASONING RESULT
    current_app.logger.info(f"reasoning result: {response}")
    return {"type": reason_type, "data": response}


def reason_and_notify_response_generator(sentence_data):
    payload = reason()
    payload['sentence_data'] = sentence_data
    response_generator_address = current_app.config.get("RESPONSE_GENERATOR_ADDRESS", None)
    if response_generator_address:
        requests.post(f"http://{response_generator_address}/process", json=payload)


def store_knowledge(triples):
    if len(triples) == 0:
        current_app.logger.warning("Triple list was empty, nothing to store...")
        return

    current_app.logger.debug(f"triples: {triples}")
    triple = triples[0]
    rdf_data = json_triple_to_rdf(triple)  # Convert JSON triple to RDF data.
    current_app.logger.debug(f"rdf_data: {rdf_data}")

    # Upload RDF data to GraphDB
    upload_rdf_data(rdf_data)
