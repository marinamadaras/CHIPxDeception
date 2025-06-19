# Experimental Setup for the Intervention

## Requirements
- Make sure bash is installed on the system (consider [using WSL2 on Windows](https://learn.microsoft.com/en-us/windows/wsl/install)).
- The system uses [Docker Compose](https://docs.docker.com/compose/install/), make sure it is installed and functioning. 
- On Mac, remove the line containing ``"credsStore"`` from ``~/.docker/config.json`` (use this command: `sed -i '' '/credsStore/d' ~/.docker/config.json && cat ~/.docker/config.json`)

## Setup
1. Update the contents of your `core-modules.yaml` file to look like this:
    ```YAML
    logger_module: logger-default
    frontend_module: front-end-intervention
    response_generator_module: response-generator-intervention
    reasoner_module: reasoning-intervention
    triple_extractor_module: text-to-triples-rule-based
    ```
2. [Create a Gemini API key](https://aistudio.google.com/app/apikey)
3. Update the `gemini_api_key` in the `config.env` file of the [reasoning-intervention](../modules/reasoning-intervention/config.env) and [response-generator-intervention](../modules/response-generator-intervention/config.env) modules with your Gemini API key.
   ```env
    GEMINI_API_KEY=<PUT_YOUR_API_KEY_HERE>
    ```
4. Update the `config.env` file in the [response-generator-intervention](../modules/response-generator-intervention/config.env) module with the chosen framing strategy to be used in response generation. You can choose a value from: `neutral`, `empathic`, or `affirming`.
   ```env
    FRAMING_STRATEGY=<PUT_YOUR_FRAMING_STRATEGY_HERE>
    ```


## Starting CHIP
- Make sure DOCKER is running.
- Navigate to the root folder of the CHIP repository.
- Use the command `./chip.sh start` to start CHIP.
- Navigate to `http://localhost:9000` and you can start conversing.

## Stopping CHIP
- Use the command `./chip.sh stop` to stop CHIP.
