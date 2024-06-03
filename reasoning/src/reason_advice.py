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
    db_connection = get_db_connection(f"http://localhost:7200/repositories/{repository}")
    return {"data": rule_based_advice(repository_name, db_connection)}


#missing connection to correct repository
#Query a list of recommended activities, sorted by values
def recommended_activities_sorted(graph, name):


    sparql = """
      PREFIX owl: 
      PREFIX rdf: 
      PREFIX rdfs: 
      PREFIX : 

      SELECT ?patient ?value (COUNT(?secondaryValue) AS ?nSecondaryValues)
      ?recommendedActivity WHERE {
        ?patient a :Patient .

        OPTIONAL {?patient :hasValue ?valueInd .
                  ?valueInd a ?value .
                  ?value rdfs:subClassOf :Value .}

        OPTIONAL {?valueInd :prioritizedOver ?secondaryValueInd .
                  ?secondaryValueInd a ?secondaryValue .
                  ?secondaryValue rdfs:subClassOf :Value .}

        OPTIONAL {?valueInd :relevantActivity ?recommendedActivity .}

        ?patient :hasRecommendedActivity ?recommendedActivity .
        MINUS {OPTIONAL {?patient :hasPhysicalActivityHabit ?recommendedActivity .}}

        FILTER(?value != :Value)
        FILTER(!bound(?secondaryValue) || ?secondaryValue != :Value)
      }
      GROUP BY ?patient ?value ?nSecondaryValues ?recommendedActivity
      ORDER BY DESC(?nSecondaryValues)
      """

#TODO MAKE THIS CONNECTION WORK, should work in connection with repository

    n = name.replace("userKG:", "")
    uri = URIRef("http://www.semanticweb.org/aledpro/ontologies/2024/2/userKG#" + n)
    res = graph.query(sparql, initBindings={'patient': uri})

    res = list(res)
    res = [(c1.n3(graph.namespace_manager), c2.n3(graph.namespace_manager),
            c3.n3(graph.namespace_manager), c4.n3(graph.namespace_manager)) for c1, c2, c3, c4 in res]
    df = pd.DataFrame(res, columns=["Patient", "Value",
                                    "NumberOfSecondaryValues", "RcommendedActivity"])
    return df.drop_duplicates("RcommendedActivity").drop(["NumberOfSecondaryValues",
                                                          "Value"],
                                                         axis=1)






def rule_based_advice(repository: str, db_connection) -> dict | None:
    """
    Formulates a question based on the presence of facts in a predetermined format.
    """

    #get the sorted list for the current user (I just put in John for now)
    recommended_activities=  recommended_activities_sorted(db_connection, John):

    # return the most preferred recommended activity
    return recommended_activities[0]
