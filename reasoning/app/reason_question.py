from SPARQLWrapper import JSON
import app.db


# Should probably somehow talk to the knowledge graph and get info from there?
# 'data' should be `None` if no advice could be formulated (can this even happen?)
def reason_question(userID: str) -> dict:
    return {"data": rule_based_question(userID)}


# TODO FdH: read required facts from external file in suitable format (ttl?)
# TODO FdH: make specific to data required for reasoning
def get_required_facts(userID: str) -> list:
    return [
        f"userKG:{userID} userKG:hasValue ?o",
        f"""
        userKG:{userID} userKG:hasValue ?o1.
        userKG:{userID} userKG:hasValue ?o2
        FILTER(?o1 != ?o2).
        ?o1 userKG:prioritizedOver ?o2  
        """,
        f"userKG:{userID} userKG:hasPhysicalActivityHabit ?o",
    ]


# TODO FdH: use suitable data formats for facts and db_connection
def query_for_presence(fact: str) -> bool:
    # turn fact into query
    query = f"""
    PREFIX userKG: <http://www.semanticweb.org/aledpro/ontologies/2024/2/userKG#>

    ASK {{
        {fact}
    }}
    """
    db_connection = app.db.get_db_connection()
    db_connection.setQuery(query)
    db_connection.setReturnFormat(JSON)
    db_connection.addParameter('Accept', 'application/sparql-results+json')
    # query db_connection for presence of fact
    response = db_connection.query().convert()

    # interpret results
    return response['boolean']


def get_missing_facts(required_facts: list) -> list:
    """
    Returns the subset of required_facts that are not in the knowledge DB.
    Returns an empty list if all required_facts are in the DB.
    """
    missing_facts = []
    for fact in required_facts:
        if not query_for_presence(fact):
            missing_facts += [fact]
    return missing_facts


def sort_missing_facts(facts: list[str]) -> list:
    """
    Returns list of facts, sorted by order in which the corresponding questions need to be asked.
    """
    # TODO FdH: simple sort that always returns list in same order
    return facts


def rule_based_question(userID: str) -> dict | None:
    """
    Formulates a question based on the presence of facts in a predetermined format.
    """
    # get list of facts required for reason_advice
    required_facts = get_required_facts(userID)

    # get list of required facts that are not in knowledge DB
    missing_facts = get_missing_facts(required_facts)

    # sort the list of missing facts
    # NOTE: sort all facts instead of selecting a single fact to support combined questions later on
    missing_facts = sort_missing_facts(missing_facts)
    if len(missing_facts) > 0:
        # return the first missing fact
        return missing_facts[0]
    else:
        return None
