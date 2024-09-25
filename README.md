# DST-API
This is reference API code and description for the DST-API project.

The main product of this repository is "POC-client.py" as the proof of concept client for the DST-API and the test-server, a simple go-program to enable easy testing of simple test-cases of a client.
The deliverables should be used in conjuction with documentation from Danmarks Statisk (DST) and is not intended to be used on its own.

POC-client.py is written as a Proof of Concept for the new API to Danmarks Statistik (DST). As such it is written more to show how to work with the API rather than to be the actual code running at a data-center.

The program is written and tested using Python 3.12.4.
Before running the program POC-client.py be sure to:
Install dependencies using: `pip install -r requirements.txt`
Set the variable **`static_url`** to the url of the server to run it against.
Then you should be set to run the program using `python POC-client.py`

For a deeper dive on the POC-client.py please refer to Documentation.txt

In the test-server folder there is a test-server written in go based on the output of swagger-codegen.
To run the test-server use 'go run main.go'
The server is not built to test resilience or to handle the complete API. The test-server is built to verify the basic functionality of a program, mainly confirming a new project through the API and a lifecycle of a project before being deleted.
The test-server works by starting a lifecycle when a project is confirmed (accepting any projectId), creating messages on the message queue sequentially after each other untill the project is marked for deletion at which point the test-server will stop sending new messages for the given project.
The test-server uses the 'patch /messages/{id}' and does not support sending in a list of ids with 'patch /messages'.
All other parts of the API are stubs that simply reply positively with no actual content.

Should a need for discussion or demonstration of POC arise then we suggest you create a ticket at our [servicedesk](https://deic.dk/hpcservicedesk).