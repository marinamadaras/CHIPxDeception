from SPARQLWrapper import SPARQLWrapper, JSON

#I took this from reason_question
def get_db_connection(address):
    """
    Returns the database connection.
    """
    connection = SPARQLWrapper(address)
    return connection


# Should probably somehow talk to the knowledge graph and get info from there?
# Return "None" if no advice could be formulated.
def reason_advice() -> dict | None:
    repository_name = 'repo-test-1'
    db_connection = get_db_connection(f"http://knowledge:7200/repositories/{repository_name}")
    return {"data": rule_based_advice(repository_name, db_connection)}


#missing connection to correct repository
#Query a list of recommended activities, sorted by values
def recommended_activities_sorted(db_connection, name):
    
    query = f"""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX : <http://www.semanticweb.org/aledpro/ontologies/2024/2/userKG#>

    SELECT DISTINCT ?patient ?recommendedActivity WHERE {{
    SELECT ?patient ?value (COUNT(?secondaryValue) AS ?nSecondaryValues) ?recommendedActivity WHERE {{
        ?patient a :Patient .
            ?patient :hasValue ?valueInd .
            ?valueInd a ?value .
            ?value rdfs:subClassOf :Value .
        
            ?valueInd :prioritizedOver ?secondaryValueInd .
            ?secondaryValueInd a ?secondaryValue .
            ?secondaryValue rdfs:subClassOf :Value .

            ?valueInd :relevantActivity ?recommendedActivity .

        ?patient :hasRecommendedActivity ?recommendedActivity .
        MINUS {{
            ?patient :hasPhysicalActivityHabit ?recommendedActivity .
        }}
        ?patient :hasName ?name .
        FILTER(?name = "{name}")
        FILTER(?value != :Value)
        FILTER(!bound(?secondaryValue) || ?secondaryValue != :Value)
        FILTER(?secondaryValue != ?value)
    }}
    GROUP BY ?patient ?value ?recommendedActivity
    ORDER BY DESC(?nSecondaryValues)}}
    """
    print(query, flush=True)
    db_connection.setQuery(query)
    db_connection.setReturnFormat(JSON)
    db_connection.addParameter('Accept', 'application/sparql-results+json')
    
    response = db_connection.query().convert()
    results = response['results']['bindings']
    print("results: ", results, flush=True)
    if len(results) == 0:
        return None
    else:
        result = results[0]
        return (result['patient']['value'], result['recommendedActivity']['value'])

def rule_based_advice(repository: str, db_connection) -> dict | None:
    """
    Formulates a question based on the presence of facts in a predetermined format.
    """

    #get the sorted list for the current user (I just put in John for now)
    recommended_activity = recommended_activities_sorted(db_connection, "John Mitchel")

    # return the most preferred recommended activity
    return recommended_activity

