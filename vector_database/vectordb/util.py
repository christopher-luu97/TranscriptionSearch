import requests
headers = {"Content-Type": "application/json"}


def process_item(args:tuple) -> list:
    """
    Vectorise input item's at embedding_api endpoint hosted in docker

    Args:
        embedding_api (str): URL to endpoint for vectorizer
        item (list): List of dictionaries
        headers (_type_, optional): _description_. Defaults to headers.

    Returns:
        list: Array containing the vectorized input
    """
    embedding_api, item, headers = args
    payload = {"transcription_document": item['text']}
    res = requests.post(embedding_api, json=payload, headers=headers)
    item['vector'] = res.json()['vectors']
    return item