# This is a CHIP Module
| Properties    |                     |
| ------------- | -------------       |
| **Name**      | Gemini Response Generator |
| **Type**      | Response Generator  |
| **Core**      | Yes |
| **Access URL**       | N/A                 |

## Description
This Response Generator uses Google's `genai` module to query Gemini for generating a response, given an appropriately built up context and the latest message that the user sent.

## Usage
Instructions:
1. Make sure to have obtained [an API key for Gemini](https://ai.google.dev/gemini-api/docs/api-key), and set the `GEMINI_API_KEY` environment variable in the module's `config.env` to it
2. Configure `core-modules.yaml` to use this module as the response generator.

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
- Internet connection for using Google Gemini