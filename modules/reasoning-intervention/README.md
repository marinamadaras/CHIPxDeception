# This is a CHIP Module
| Properties    |                     |
| ------------- | -------------       |
| **Name**      | Demo Reasoning |
| **Type**      | Reasoner  |
| **Core**      | Yes |
| **Access URL**       | N/A                 |

## Description
This Reasoner is intended as a demo module, for following the demo scenario outlined in `demo_scenario.md`. It queries the `knowledge-demo` GraphDB database to infer suitable activities to partake in for a diabetes patient by the name "John", based on his values and preferences.

To obtain these values and preferences, it also inserts RDF triples into `knowledge-demo` based on information obtained from the Triple Extractor.

## Usage
Instructions:
1. Configure `core-modules.yaml` to use this module as the reasoner.

## Input/Output
Communication between the core modules occurs by sending a POST request to the `/process` route with an appropriate body, as detailed below.

### Input from `Triple Extractor`
```JSON
{
    "sentence_data": {
        "patient_name": <string>,   // The name of the user currently chatting
        "sentence": <string>,       // The sentence that the user submitted
        "timestamp": <string>       // The time at which the user submitted the sentence (ISO format)
    },
    "triples": [
        {
            "subject":<string>, 
            "object": <string>, 
            "predicate":<string>
        },
        ...
    ]
}
```
### Output to `Response Generator`
```JSON
	{
        "sentence_data": {
            "patient_name": <string>,   // The name of the user currently chatting.
            "sentence": <string>,       // The sentence that the user submitted.
            "timestamp": <string>       // The time at which the user submitted the sentence (ISO format).
        },
		"type": <string: Q|A>,          // Whether the reasoner decided to give an answer (A) or to request more information (Q).
		"data": <dict>                  // A dict containing the output of the reasoner.
	}
```
## API (routes, descriptions, models)
- [GET] `/`: default 'hello' route, to check whether the module is alive and kicking.
---
- [POST] `/store`: stores RDF triples into the knowledge based on a list of SPO triples.

**Model**
```JSON
    [  // An array of SPO triples.
        {
            "subject":<string>, 
            "object": <string>, 
            "predicate":<string>
        },
        ...
    ]
```
---
- [POST] `/reason`: reasons over the currently available knowledge based on the sentence submitted by the user.

**Model**
```JSON
        "sentence_data": {
            "patient_name": <string>,   // The name of the user currently chatting.
            "sentence": <string>,       // The sentence that the user submitted.
            "timestamp": <string>       // The time at which the user submitted the sentence (ISO format).
        },
``` 
---

## Internal Dependencies
- `knowledge-demo`

## Required Resources
None.