# This file contains the code required to vectorize an input string
# There are calls to an API that has a sentence-embedding model 
# This model has been wrapped into an API with FastAPI and dockerized

import requests

headers = {"Content-Type": "application/json"}

class questionObj():
    """
    This class will contain the queries
    """
    def __init__(self, query:str):
        self.query = {"text":query}

def process_item(item:list, embedding_api:str, headers=headers) -> list:
    """_summary_

    Args:
        item (list): _description_
        embedding_api (str): _description_
        headers (_type_, optional): _description_. Defaults to headers.

    Returns:
        list: _description_
    """
    payload = {"transcription_document": item['text']}
    res = requests.post(embedding_api, json=payload, headers=headers)
    item['vector'] = res.json()['vectors']
    return item