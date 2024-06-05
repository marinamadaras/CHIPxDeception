from flask import Flask, request, jsonify
import requests
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
def json_triple_to_rdf(triples):
    # Define namespaces
    user_kg = Namespace("http://www.semanticweb.org/aledpro/ontologies/2024/2/userKG#")

    # Create an RDF graph
    g = Graph()
    g.bind("userKG", user_kg)

    # Extract subject, predicate, and object from the JSON data
    subject = triples.get("subject")
    predicate = triples.get("predicate")
    obj = triples.get("object")
    print("triple:", subject, predicate, obj, flush=True)

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
    print(f"Triples received: {request.json}", flush=True)
    json_data = request.json
    
    triples = json_data['triples']
    if len(triples) > 0:
        print('triples', triples, flush=True)
        triple = triples[0]
        # Convert JSON triple to RDF data
        rdf_data = json_triple_to_rdf(triple)
        print("rdf_data:", rdf_data, flush=True)
        
        repository_url = "http://knowledge:7200"  # Update as needed
        repository_name = "repo-test-1"  # Update as needed
        
        # Upload RDF data to GraphDB
        response = upload_rdf_data(repository_url, repository_name, rdf_data)
        if response.status_code == 204:
            result = jsonify({"message": "Data uploaded successfully!"}), 200
        else:
            result = jsonify({"error": f"Failed to upload data: {response.status_code}, {response.text}"}), 500
    else:
        result = ({"message": "Empty triple set received"}), 200

    # IF DONE, START REASONING (should query knowledge base somehow)
    reason_and_notify_response_generator()

    return result


# Note that we first check if we can give advice, and if that is "None",
# then we try to formulate a question instead.
@app.route('/reason')
def reason_and_notify_response_generator():
    response = reason_advice()
    print("advice response:", response, flush=True)
    reason_type = "A"
    if (not response or not response['data']):
        print("Could not give advice, asking question instead", flush=True)
        reason_type = "Q"
        response = reason_question()

    # SEND REASONING RESULT
    print("reasoning result: ", response, flush=True)
    payload = {"type": reason_type, "data": response}
    requests.post("http://response-generator:5000/submit-reasoner-response", json=payload)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
