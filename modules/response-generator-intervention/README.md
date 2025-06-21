# Response Generator
| Properties    |                                 |
| ------------- |---------------------------------|
| **Name**      | Intervention Response Generator |
| **Type**      | Response Generator              |


## Description
This response generator was developed to support conversations in the context of the BSc Project **To deceit or self-deceit?**
Most of the logic was **copied** from the `response-generator-gemini` module, and then adapted for the use-case. 

## Pre-requisites for Setup
1. Make sure to have obtained [an API key for Gemini](https://ai.google.dev/gemini-api/docs/api-key), and set the `GEMINI_API_KEY` environment variable in the module's `config.env` to it
2. Configure `core-modules.yaml` to use this module as the response generator.

## Framing Strategies
The response generator uses a framing strategy to generate responses. The available strategies are:
- `neutral`: responses use a neutral tone, providing information as is.
- `empathic`: responses are generated with a cognitively empathic and soft tone, attempting to understanding the user better.
- `affirming`: responses are generated with an affirming tone, based on the idea of self-affirmations to validate the user's personal values.

Only one can be used at a time, and it is set in the `config.env` file of the module. 


### Input from `Reasoner`
```JSON
	{
        "sentence_data": {              // This is actually ignored.
            "patient_name": <string>,   
            "sentence": <string>,       
            "timestamp": <string>      
        },
  
        "type": <string>,               // The type of response being generated, corresponds to "response_type" in the data.
        "data":                         // The data to be used by the response generator.
            {                     
              "response_type": <string>,                       // The type of response to be generated, one of ack, question, answer, greeting, closing.
              "value": <string>,                               // The content that the response should contain, as atomic as possible.
              "reason": <string>,                              // The LLM's justification for the given response.
              "soft_self_management_indicators": [<string>],   // A list of inferred indicators that might indicate struggle with self-management.
              "personal_values": [<string>]                    // A list of personal values that the user has expressed in (previous) conversations.
            }       
	}
```
### Output to `Front End`
```JSON
    {
        "message": <string>             // The generated message.
    }
```

## Internal Dependencies
- reasoning-intervention

## Required Resources
- Internet connection
- Gemini API Key