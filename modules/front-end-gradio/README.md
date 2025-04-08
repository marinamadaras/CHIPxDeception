# This is a CHIP Module
| Properties    |                     |
| ------------- | -------------       |
| **Name**      | Gradio Front-End |
| **Type**      | Front-End  |
| **Core**      | Yes |
| **Access URL**       | http://localhost:8000/gradio/ |

## Description
This is the old Gradio front-end. Since this module never got refactored, it is still based on an old format. It runs both the front-end and the accompanying backend in the same file. It features a chat input, that waits for a response from the response generator and then shows it.

It is not recommended to use this, but it is still nice to have it as an example regardless.

## Usage
Instructions:
1. Configure `core-modules.yaml` to use this module as the front-end.

## Input/Output
Since this module still follows the old format, it uses a different route for dealing with input:

### Input from `Response Generator` via `/response` route
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

- [GET] `/ping/<name>`: pings another module in the system, by triggering their `hello` route.

- [GET] `/ping/<name>/<endpoint>`: allows you to reach the other routes of the other modules, useful for debugging.


## Internal Dependencies
None.

## Required Resources
None.