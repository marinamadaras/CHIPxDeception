# This is a CHIP Module
| Properties    |                     |
| ------------- | -------------       |
| **Name**      | Quasar Front-End |
| **Type**      | Front-End  |
| **Core**      | Yes |
| **Access URL**       | http://localhost:9000/ |

## Description
This is the main front-end that the demo uses. It features a chat window with scrollable history, and a panel that gives a view of the GraphDB knowledge base.

It is built in Quasar (based on Vue3), and has an accompanying backend that handles communication with the rest of the modules, through HTTP requests and SSE (for communicating back to the front-end).

## Usage
Instructions:
1. Configure `core-modules.yaml` to use this module as the front-end.

## Input/Output
Communication between the core modules occurs by sending a POST request to the `/process` route with an appropriate body, as detailed below.

### Input from `Response Generator`
```JSON
    {
        "message": <string>             // The generated message.
    }
```

### Output to `Triple Extractor`
```JSON
{
    "patient_name": <string>,   // The name of the user currently chatting
    "sentence": <string>,       // The sentence that the user submitted
    "timestamp": <string>       // The time at which the user submitted the sentence (ISO format)
}
```

## API (routes, descriptions, models)
- [GET] `/`: default 'hello' route, to check whether the module is alive and kicking.

- [POST] `/submit`: used to submit a sentence from the UI to the backend. See `Output` above for format.


## Internal Dependencies
- `redis` - for SSE
- `knowledge` - for GraphDB visualization and DB

## Required Resources
None.