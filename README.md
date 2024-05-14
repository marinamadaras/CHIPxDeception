# CHIP DEMO

## How to run
0. Clone this repository somehow (preferably with `git` or `Fork` if you want to make additions, but to just run it you can also just download a zip)
1. Make sure you have Docker Desktop installed and properly configured somehow
2. Run the following command in your favorite terminal application window in the root folder of the project: `docker-compose build`. 

The first time you do this it may take a while, as it needs to download all the images and build the containers.

3. As soon as that is done, you may run `docker-compose up`, to bring the whole system up.

If this succeeded, you can go to `localhost:8000` in your favorite browser, the system should welcome you. The Gradio interface can be accessed at `localhost:8000/gradio`. You may initialize the knowledge repository with `localhost:8000/init` and load the initial knowledge graph with `localhost:8000/load_kg`.

In the Docker Desktop dashboard, you can also see all of the containers and their status, and you may click them to inspect their logs, or even login to perform commands on them. See this guide for more info: https://docs.docker.com/desktop/use-desktop/


## Resetting and making changes
In order to reset the system entirely and take it down, you should use `docker-compose down -v`. It is important to include the `-v` flag, otherwise the underlying GraphDB data will not be reset and persist instead. You can then bring the system up again by using `docker-compose up`.

Normally, if you make changes to the code in the `src` folder, they should automatically transfer to your container as it is running. If this is not case, you can run the following commands in sequence to propagate your code updates:

```
docker-compose down -v
docker-compose build
docker-compose up
```
> NOTE: Changes to the front-end currently do not propagate, so you need to execute the above three commands in sequence in order to make them appear. You can also just use `CTRL+C` (on windows) on the terminal that hosts docker-compose to take the system down, though this will NOT take the GraphDB volume down.


## General terminology and project setup
- Each of the folders in this project represent a "module"; a separate component in the system that can talk to the other components.

- We use docker-compose to launch all these modules together; each of them will be represented by one container.

- Each of these containers are isolated little systems based on images specified in their `Dockerfile` that run their corresponding module under an API. 

- You can see an API as some sort of access point, a gateway to either send data (POST), or to trigger some code or get data (GET). The URL/link that is used for doing this is called a "route". For instance, the front-end module has the `/gradio` route, which you can browse to in order to see the UI. This idea of "browsing" to a "route" is known as "sending a request". So in this system, the containers are sending `GET` and `POST` requests to one another in order to communicate.

- In practice, the main difference between `GET`and `POST` is that you can send additional data in a `POST` request, which is stored in the "body" of the request. This allows us to pass `JSON` and files around.

- The `docker-compose.yml` in the root folder shows the names of each of the containers, and the ports that they expose. Usually, a module can be spoken to via: `http://<module-name>:5000/<route>`.

- The "image" that they use is the recipe for the system. That `Dockerfile` file that you can find in each of the module's folders basically represents that recipe. 

- The `FROM` clause in those files tells you what the "base" recipe is that the image is based on, the following format `<image>:<tag>`. Nearly all `Dockerfile` files in the project are currently using `python:3-slim`, but you can change this according to your needs, e.g. `python:3.9-slim`. You can find all possible tags here: https://hub.docker.com/_/python/tags?page=&page_size=&ordering=&name=3.9


## Module route overview
This is a list of the modules and the routes they expose.

### `front-end` (visible to the host! Use `http://localhost:5000/<route>`)
- [GET] `/`: The base route, should welcome you to the system
- [GET] `/init`: Initializes the GraphDB knowledge database
- [GET] `/ping`: Allows you to ping other modules in the system, making them welcome you
- [POST] `/response`: Expects a response from the `response-generator` module here.
	- Expected format (this might change depending on what we need): 
	```json
		{
			"reply": <str>
		}
	```

### `knowledge`
This module has its own API which is documented at: https://graphdb.ontotext.com/documentation/10.2/using-the-graphdb-rest-api.html

It's a bit tricky to use however... Still in the process of figuring it out.


### `logger`
The logger is currently not utilized yet.

- [GET] `/`: The base route, welcomes you to the module
- [GET] `/log/<line>`: Sends a line of text to the logger


### `text-to-triples`
The `front-end` posts sentence data to this module, and this module then posts that to the `reasoning` module.

- [GET] `/`: The base route, welcomes you to the module
- [POST] `/new-sentence`: `front-end` posts new sentences input by the user to this route.
	- Expected format:
	```json
    {
        "patient_name": <str>,
        "sentence": <str>,
        "timestamp": <str>
    }
	```

### `reasoning`
The reasoning module receives a list of triples from the `text-to-triples` modules, performs some computations and communications with the `knowledge` module based on this (should store the new knowledge among other things), and then posts a reasoning result to the `response-generator` module.

The `reason_advice.py` and `reason_question.py` files should contain the code necessary to infer advice resp. a question based on the knowledge in GraphDB.

- [GET] `/`: The base route, welcomes you to the module
- [POST] `/query-knowledge`: Allows modules to query the knowledge, not implemented yet.
	- Expected format: TBD
- [POST] `/store-knowledge`: Allows modules to store new knowledge, and notifies the response-generator that it should formulate a response.
	- Expected format:
	```json
	{
		"triples": [
			{
				"subject":<str>, 
				"object": <str>, 
				"predicate":<str>
			},
			...
		]
	}
	```

### `response-generator`
This module is responsible for formulating a human-readable response, based on the sentence received from the front-end and the data received from the reasoner.

- [GET] `/`: The base route, welcomes you to the module
- [POST] `/submit-sentence`: Allows the front-end to submit a sentence sent by a patient/user to this module.
	- Expected format:
	```json
    {
        "patient_name": <str>,
        "sentence": <str>,
        "timestamp": <str>
    }
	```
- [POST] `/submit-reasoner-response`: Allows the reasoning module to submit a reasoning type and data that goes with it.
	- Expected format (this might change depending on what we need):
	```json
	{
		"type": <str: `Q|A`>, 
		"data": <dict>
	}
	```