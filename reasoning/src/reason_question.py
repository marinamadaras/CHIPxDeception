from SPARQLWrapper import SPARQLWrapper, JSON

def get_db_connection(address):
    """
    Returns the database connection.
    """
    connection = SPARQLWrapper(address)
    return connection

# Should probably somehow talk to the knowledge graph and get info from there?
# Return "None" if no question could be formulated (can this even happen?)
def reason_question() -> dict | None:
    repository_name = 'repo-test-1'
    db_connection = get_db_connection(f"http://localhost:7200/repositories/{repository}")
    return {"data": rule_based_question(repository_name, db_connection)}

# TODO FdH: read required facts from external file in suitable format (ttl?)
# TODO FdH: make specific to data required for reasoning
def get_required_facts() -> list:
    return [
        "wine:SchlossRothermelTrochenbierenausleseRiesling wine:hasSugar ?o", # a fact that is present
        "wine:SchlossRothermelTrochenbierenausleseRiesling wine:hasPrice ?o", # a fact that is not present
        "wine:SchlossRothermelTrochenbierenausleseRiesling wine:hasRating ?o", # a fact that is not present
    ]

# TODO FdH: use suitable data formats for facts and db_connection
def query_for_presence(fact: str, db_connection) -> bool:
    # turn fact into query
    query = f"""
    PREFIX wine: <http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#>

    ASK {{
        {fact}
    }}
    """
    db_connection.setQuery(query)
    db_connection.setReturnFormat(JSON)
    db_connection.addParameter('Accept', 'application/sparql-results+json')
    # query db_connection for presence of fact
    response = db_connection.query().convert()

    # interpret results
    return response['boolean']

def get_missing_facts(repository: str, db_connection, required_facts: list) -> list:
    """
    Returns the subset of required_facts that are not in the knowledge DB.
    Returns an empty list if all required_facts are in the DB.
    """
    missing_facts = []
    for fact in required_facts:
        if not query_for_presence(fact, db_connection):
            missing_facts += [fact]
    return missing_facts

def sort_missing_facts(facts: list[str]) -> list:
    """
    Returns list of facts, sorted by order in which the corresponding questions need to be asked.
    """
    # TODO FdH: simple sort that always returns list in same order
    return facts

def rule_based_question(repository: str, db_connection) -> dict | None:
    """
    Formulates a question based on the presence of facts in a predetermined format.
    """
    # get list of facts required for reason_advice
    required_facts = get_required_facts()

    # get list of required facts that are not in knowledge DB
    missing_facts = get_missing_facts(repository, db_connection, required_facts)

    # sort the list of missing facts
    # NOTE: sort all facts instead of selecting a single fact to support combined questions later on
    missing_facts = sort_missing_facts(missing_facts)

    # return the first missing fact
    return missing_facts[0]