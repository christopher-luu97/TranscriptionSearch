# Offline Vector Database for Search

## Description

The /vectordb folder contains the code used to create and update the Weaviate schema with appropriate data.

The main.py file is ran to update contents within the existing Weaviate instance, allowing us to perform CREATE, READ, UPDATE, DELETE like statements (if following SQL syntax) in the vector database.

This should be ran when new data is to be vectorized, so that the frontend be used.

The provided data should all be contained within a folder for batch processing.

## Requirements

Have a weaviate instance already up and running at http://localhost:8080 or alternatively, specify your own endpoint to your weaviate instance in main.py.

Have the embedding model API dockerized in a container and exposed at "http://127.0.0.1:8200/embed" or alternatively, provide your own endpoint, however, it is recommended to use the models performed here. Navigate to the /models/embeddings folder to see how to set this up.

## TODO

In the future, I want to implement this as a feature to the frontend so the user has an in-browser method of performing updates instead of relying on the execution of a Python script that has specific requirements to be installed. (Or maybe I could just use another docker container with an API)
