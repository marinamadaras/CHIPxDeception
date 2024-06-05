Demo scenario

# Setting up
1. Follow all instructions in the ``README.md`` to install the system
2. Call ``restart.sh`` for a fresh start of the system
2. Browse to [localhost:8000/init](http://localhost:8000/init) to initialize the KG graph

# Background
In the scenario, a user named John interacts with the system.
A lot is already known about John, so part of the inference has already happened to conclude:
* John is a diabetes patient
* John needs to do physical exercise in order to manage his diabetes
* John upholds certain values in life, you can see them by running a query on the database

Some things are not known yet about John, such as which values he values more or less than others.

# Dialogue
Here is an example dialogue:
User: Hi
System: Hi, John

User: What do you recommend?
System: John, how do you prioritize your values?

User: I prioritize security over work
System: How about 'activity balance', John?
(Explanation: security relates to feeling comfortable and is associated with activities that can be done at home, such as balance activities done alone at home.)

User: I prioritize family over security
System: How about 'activity cycling', John?
(Explanation: the system infers that John should go cycling, as this can be done with family)

User: Thanks
System: Goodbye


(You will now have to kill the system with CTRL-C and restart it with ``restart.sh`` and by visiting [localhost:8000/init](http://localhost:8000/init))


## Scenario queries
These are some queries that show interesting behaviors of the system.

Start the system (see above) and go to [the graphdb workbench](http://localhost:7200/sparql).
Tip: you can give your queries names and use the '+' sign to show multiple queries in separate tabs.

A query that shows John's recommended activities
```sparql
PREFIX : <http://www.semanticweb.org/aledpro/ontologies/2024/2/userKG#>

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?patient ?activity WHERE {
        ?patient a :Patient .
		?patient :hasName ?name .
        FILTER(str(?name) = "John Mitchel").
        
        ?patient :hasRecommendedActivity ?activity .   
    }
```

A query that shows John's values
```sparql
PREFIX : <http://www.semanticweb.org/aledpro/ontologies/2024/2/userKG#>

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?patient ?value WHERE {
        ?patient a :Patient .
		?patient :hasName ?name .
        FILTER(str(?name) = "John Mitchel")
        
        ?patient :hasValue ?valueInd .
        ?valueInd a ?value .
        ?value rdfs:subClassOf :Value .
		FILTER(?value != :Value) .
		FILTER(!bound(?secondaryValue) || ?secondaryValue != :Value) .
    }
```

A query that shows how Johns values are prioritized
```sparql
PREFIX : <http://www.semanticweb.org/aledpro/ontologies/2024/2/userKG#>

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?patient (?value as ?prioritizedValue) ?otherValue WHERE {
        ?patient a :Patient .
		?patient :hasName ?name .
        FILTER(str(?name) = "John Mitchel") .
        
        ?patient :hasValue ?valueInd .
        ?valueInd a ?value .
        ?value rdfs:subClassOf :Value .
    	
    	?patient :hasValue ?otherValueInd .
    	?otherValueInd a ?value.
    	?value rdfs:subClassOf :Value .
    
    	?value :prioritizedOver ?otherValue .
    
		FILTER(?value != :Value) .
    	FILTER(?otherValue != ?value) .
   		FILTER(?otherValue != :Value) .
    }
```