from flask import Flask, request, jsonify
import requests
import json
from reason_advice import reason_advice
from reason_question import reason_question
from rdflib import Graph, Namespace, URIRef, Literal

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello():
    return 'Hello, I am the reasoning module!'


@app.route('/query-knowledge', methods=['POST'])
def query_knowledge():
    pass

# Function to convert a JSON triple to RDF format
def json_triple_to_rdf(json_data):
    # Define namespaces
    ex = Namespace("http://example.org/ontology#")
    data = Namespace("http://example.org/data#")

    # Create an RDF graph
    g = Graph()
    g.bind("ex", ex)
    g.bind("data", data)

    # Extract subject, predicate, and object from the JSON data
    subject = json_data.get("subject")
    predicate = json_data.get("predicate")
    obj = json_data.get("object")

    # Construct subject, predicate, and object URIs
    subject_uri = data[URIRef(subject.replace(" ", ""))]
    predicate_uri = ex[URIRef(predicate)]
    if isinstance(obj, (int, float)):
        object_uri = Literal(obj)
    else:
        object_uri = data[URIRef(obj.replace(" ", ""))]

    # Add the triple to the graph
    g.add((subject_uri, predicate_uri, object_uri))

    # Serialize the graph to Turtle format and return
    return g.serialize(format="turtle")


# Function to upload RDF data to GraphDB
def upload_rdf_data(repository_url, repository_name, rdf_data, content_type='application/x-turtle'):
    """
    Upload RDF data to a GraphDB repository using the REST API.

    :param repository_url: URL of the GraphDB instance
    :param repository_name: Name of the GraphDB repository
    :param rdf_data: RDF data in string format (Turtle, RDF/XML, etc.)
    :param content_type: MIME type of the RDF data (default is Turtle)
    :return: Response object
    """
    headers = {
        'Content-Type': content_type
    }

    # Construct the full endpoint URL
    endpoint = f"{repository_url}/repositories/{repository_name}/statements"

    # Send a POST request to upload the RDF data
    response = requests.post(endpoint, data=rdf_data, headers=headers)

    return response

@app.route('/store-knowledge', methods=['POST'])
def store_knowledge():
    # Get JSON data from the POST request
    json_data = request.json
    
    # Convert JSON triple to RDF data
    rdf_data = json_triple_to_rdf(json_data)
    
    repository_url = "http://localhost:7500"  # Update as needed
    repository_name = "userKG_repo"  # Update as needed
    
    # Upload RDF data to GraphDB
    response = upload_rdf_data(repository_url, repository_name, rdf_data)
    if response.status_code == 204:
        return jsonify({"message": "Data uploaded successfully!"}), 200
    else:
        return jsonify({"error": f"Failed to upload data: {response.status_code}, {response.text}"}), 500


    print(f"Triples received: {request.json}", flush=True)

    # IF DONE, START REASONING (should query knowledge base somehow)
    reason_and_notify_response_generator()

    return 'OK'


# Note that we first check if we can give advice, and if that is "None",
# then we try to formulate a question instead. 
def reason_and_notify_response_generator():
    response = reason_advice()
    reason_type = "A"
    if (not response):
        reason_type = "Q"
        response = reason_question()

    # SEND REASONING RESULT
    payload = {"type": reason_type, "data": response}
    requests.post("http://response-generator:5000/submit-reasoner-response", json=payload)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
