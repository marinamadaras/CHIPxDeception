# This is a CHIP Module
| Properties    |                     |
| ------------- | -------------       |
| **Name**      | Medalpaca Response Generator Intel CPU |
| **Type**      | Response Generator  |
| **Core**      | Yes |
| **Access URL**       | N/A                 |

## Description
This Response Generator uses the `transformers` library in combination with PyTorch in order to locally run and query an LLM based on `medalpaca-7b` for response generation. By default, a GPU with CUDA is expected to be present, however you may configure the `CUDA_VISIBLE_DEVICES` environment variable in the `compose.yml` file to an empty string `""` instead of `0`, which will cause PyTorch to fall back on using only the CPU. Naturally, this is very slow (~1-5 minutes per response).

Note that the implementation is very incomplete as of yet. This is just a proof-of-concept of running and querying an LLM intended for medical purposes locally.

**WARNING:** Starting the module for the first time will build the image that the module uses, which downloads all pre-requisites and pre-downloads + caches the model, which may take up a very large amount of time (up to an hour) and storage (~40GB).

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
For CPU only:
- At least 32GB RAM
- At least 30GB of free disk space

For GPU usage:
- GPU + driver with CUDA support 
- At least 32GB of VRAM
