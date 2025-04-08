# This is a CHIP Module
| Properties    |                     |
| ------------- | -------------       |
| **Name**      | Rule-Based Triple Extractor |
| **Type**      | Triple Extractor  |
| **Core**      | Yes |
| **Access URL**       | N/A |

## Description
A rule-based triple extractor module, using nltk to disect a sentence and extract triples from it. It is compatible with the demo knowledge, in that it transforms the extracted predicates into terms that the knowledge database understands.

## Usage
Instructions:
1. Configure `core-modules.yaml` to use this module as the triple extractor.

## Input/Output
Communication between the core modules occurs by sending a POST request to the `/process` route with an appropriate body, as detailed below.

### Input from `Front-End`
```JSON
{
    "patient_name": <string>,   // The name of the user currently chatting
    "sentence": <string>,       // The sentence that the user submitted
    "timestamp": <string>       // The time at which the user submitted the sentence (ISO format)
}
```

### Output to `Reasoner`
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

## API (routes, descriptions, models)
- [GET] `/`: default 'hello' route, to check whether the module is alive and kicking.


## Internal Dependencies
None.

## Required Resources
None.
