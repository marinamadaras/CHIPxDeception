# This is a CHIP Module
| Properties    |                     |
| ------------- | -------------       |
| **Name**      | Demo Response Generator |
| **Type**      | Response Generator  |
| **Core**      | Yes |
| **Access URL**       | N/A                 |

## Description
This Response Generator is intended as a demo module, for following the demo scenario outlined in `demo_scenario.md`. It scans the output obtained by the reasoner and then picks a pre-defined response based on that.

## Usage
Instructions:
1. Configure `core-modules.yaml` to use this module as the response generator.

## Input/Output
Communication between the core modules occurs by sending a POST request to the `/process` route with an appropriate body, as detailed below.

### Input from `Reasoner`
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
### Output to `Front End`
```JSON
    {
        "message": <string>             // The generated message.
    }
```
## API (routes, descriptions, models)
- [GET] `/`: default 'hello' route, to check whether the module is alive and kicking.

## Internal Dependencies
None.

## Required Resources
None.