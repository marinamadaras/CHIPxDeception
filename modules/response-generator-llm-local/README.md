# This is a CHIP Module
| Properties    |                     |
| ------------- | -------------       |
| **Name**      | Medalpaca Response Generator CUDA |
| **Type**      | Response Generator  |
| **Core**      | Yes |
| **Access URL**       | N/A                 |

## Description
This Response Generator uses the `transformers` library in combination with PyTorch in order to locally run and query an LLM based on `medalpaca-7b` for response generation. By default, a GPU with CUDA is expected to be present, however you may configure the `CUDA_VISIBLE_DEVICES` environment variable in the `compose.yml` file to an empty string `""` instead of `0`, which will cause PyTorch to fall back on using only the CPU. Naturally, this is very slow (~1-5 minutes per response). For now GPU-support in docker is only confirmed to be working on Windows in WSL2.

Note that the implementation is very incomplete as of yet. This is just a proof-of-concept of running and querying an LLM intended for medical purposes locally. The response generator will attempt to "properly" respond to greetings and to any variation of the phrase "What do you recommend?"", where the LLM will be used to formulate a reponse.

**WARNING:** Starting the module for the first time will build the image that the module uses, which downloads all pre-requisites and pre-downloads + caches the model, which may take up a very large amount of time (up to an hour) and storage (~40GB).

## Usage
Instructions:
1. Open `compose.yml` in this folder, and configure your CUDA version by adjusting the `CUDA_MAJOR`.`CUDA_MINOR` values. You can discover your CUDA version and whether it is functioning in Docker at all by running the following command: `sudo docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi`.
2. In the same file, also configure the LLM to use by changing the value of `MODEL_NAME`, by default this is `medalpaca/medalpaca-7b`. Changing this will trigger a redownload of the model during build, which can take quite long.
3. Configure `core-modules.yaml` to use this module as the response generator.

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

## Required Resources (for medalpaca/medalpaca-7b)
For CPU only:
- At least 32GB RAM
- At least 30GB of free disk space

For GPU usage:
- GPU + driver with CUDA support 
- Latest Docker (compose) version
- At least 8GB of VRAM
