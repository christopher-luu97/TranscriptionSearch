# Offline Vector Database for Search

## Description

The /Databaser folder contains the code used to create and update the Weaviate schema with appropriate data.

The main.py file is ran to update contents within the existing Weaviate instance, allowing us to perform CREATE, READ, UPDATE, DELETE like statements (if following SQL syntax) in the vector database.

This should be ran when new data is to be vectorized, so that the frontend be used.

The provided data should all be contained within a folder for batch processing.

## TODO
In the future, I want to implement this as a feature to the frontend so the user has an in-browser method of performing updates instead of relying on the execution of a Python script that has specific requirements to be installed. (Or maybe I could just use another docker container with an API)

