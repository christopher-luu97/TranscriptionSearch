# Offline Vector Database for Search

## Demonstration Video:
Link: https://youtu.be/1Rlz3VlKcsk

## Description

This repository contains code to build a web application to search Transcriptions using Weaviate.. The main intent is to provide users with an interface for offline (or online if deployed) vector database that they can use to perform searches independently. The backend uses Django for an API, another dockerized API for sentence-embedding to vectorize text, as well ass code to allow for the downloading of youtube videos and subsequent transcription (found in a google colab for faster speed).

## Features
- Natural language search functionality using Weaviate as the vector database.
- Keyword/phrase search in transcripts with highlighting
- Time search in transcripts with highlighting
- Dockerized FastAPI of the sentence-embedding model that can be hosted elsewhere for scalability
- Insert transcripts to a weaviate instance via CLI Python scripts
- Download and transcribe youtube videos to be inserted to weaviate instance via CLI or through the supplied notebook. (Needs manual editing by user)

<h2>System Design</h2>
<p>This system design is based off of what has been done and what needs to be done. It includes features and how things talk to each other.</p>
<img src="./system_design/design_v1.jpeg"/>
