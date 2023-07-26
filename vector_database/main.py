from vectordb.vectordb import vectorDB
import json
import os

if __name__ == '__main__':
    DATA_PATH = input("Input full data path: ")
    endpoint = "http://localhost:8080"
    schema_file = os.path.join(os.getcwd(), "vectordb",'schema.json')
    embedding_api = "http://127.0.0.1:8200/embed"
    vb = vectorDB()
    vb.start(endpoint)
    vb.create_schema(schema_file)
    vb.get_file_paths(DATA_PATH)
    vb.batch_insert(embedding_api)
    result = vb.client.query.get(
            "Transcriptions", ["title","text", "start_time","end_time"]
        ).do() # Additional parameters of probability returned
    print(json.dumps(result, indent=4))