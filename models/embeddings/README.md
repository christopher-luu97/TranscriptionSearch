# Sentence Embedding API

## Description

This embeddings folder contains a simple api of a sentence embedding model using FastAPI. The user should build the dockerfile and then call this api from wherever else they need.

## Setup

CD to this directory in the terminal and execute the following steps.

Build:
docker build -f embedding.DOCKERFILE -t embedding_api_build:latest .

Then to run:
docker run -p 8200:8200 embedding_api_build:latest
