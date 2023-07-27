import json
import os
import pytest
from weaviate.batch import Batch
from vector_database.vectordb.vectordb import vectorDB

@pytest.fixture
def data_folder(tmpdir):
    """
    Fixture to create a temporary data folder with sample JSON files.
    """
    data_path = tmpdir.mkdir("data_folder")
    file1_content = {
        "segments": [
            {
                "start": 0.379,
                "end": 0.841,
                "text": "Ah, OK.",
                "words": [
                    {"word": "Ah,", "start": 0.379, "end": 0.459, "score": 0.706},
                    {"word": "OK.", "start": 0.761, "end": 0.841, "score": 0.273}
                ],
                "id": "0_Lecture 3: Editors (vim) (2020).mp3",
                "title": "Lecture 3_ Editors (vim) (2020)"
            }
        ]
    }
    file2_content = {
        "segments": [
            {
                "start": 1.675,
                "end": 2.455,
                "text": "Cool.",
                "words": [
                    {"word": "Cool.", "start": 1.675, "end": 1.855, "score": 0.444}
                ],
                "id": "1_Lecture 3: Editors (vim) (2020).mp3",
                "title": "Lecture 3_ Editors (vim) (2020)"
            }
        ]
    }

    file1_path = data_path.join("file1.json")
    file2_path = data_path.join("file2.json")

    file1_path.write(json.dumps(file1_content))
    file2_path.write(json.dumps(file2_content))

    return str(data_path)

def test_vectorDB_creation():
    vb = vectorDB()
    assert isinstance(vb, vectorDB)

def test_start_method():
    vb = vectorDB()
    vb.start("http://localhost:8080")
    assert vb.client.url == "http://localhost:8080"

def test_create_schema_method():
    vb = vectorDB()
    schema = {
        "classes": [
            {
                "class": "Transcriptions",
                "description": "Transcriptions",
                "properties": [
                    {
                        "name": "title",
                        "dataType": ["string"]
                    },
                    {
                        "name": "id_title",
                        "dataType": ["string"]
                    },
                    {
                        "name": "text",
                        "dataType": ["string"]
                    },
                    {
                        "name": "start_time",
                        "dataType": ["number"]
                    },
                    {
                        "name": "end_time",
                        "dataType": ["number"]
                    },
                    {
                        "name": "vector",
                        "dataType": ["vector"]
                    }
                ]
            }
        ]
    }
    vb.start("http://localhost:8080")
    vb.create_schema(schema)
    assert len(vb.client.schema.get()) == 1

def test_get_file_paths_method(data_folder):
    vb = vectorDB()
    vb.get_file_paths(data_folder)
    assert len(vb.TRANSCRIPTS) == 2
    assert "file1.json" in vb.TRANSCRIPTS
    assert "file2.json" in vb.TRANSCRIPTS

def test_embedding_api_url_method():
    vb = vectorDB()
    vb.embedding_api_url("http://example.com")
    assert vb.embedding_api == "http://example.com"

class MockWeaviateClient:
    def __init__(self):
        self.schema = MockWeaviateSchema()
        self.batch = MockBatch()

class MockWeaviateSchema:
    def get(self):
        return []

    def create(self, schema):
        pass

class MockBatch:
    def __init__(self):
        self.data_objects = []
        self.references = []

    def add_data_object(self, data_object, class_name, uuid, vector):
        self.data_objects.append({
            "data_object": data_object,
            "class_name": class_name,
            "uuid": uuid,
            "vector": vector
        })

    def create_objects(self):
        pass

    def create_references(self):
        pass

@pytest.fixture
def vector_db():
    """
    Fixture to create a vectorDB instance with a mock weaviate client.
    """
    db = vectorDB()
    db.client = MockWeaviateClient()
    return db

def test_add_transcription(vector_db):
    # Sample transcription data
    transcription_data = {
        "title": "Sample Title",
        "id": "sample_id",
        "text": "Sample transcription text",
        "start": 0.0,
        "end": 1.0,
        "vector": [0.1, 0.2, 0.3]
    }

    # Create a mock batch
    batch = Batch()

    # Call the add_transcription method
    transcription_id = vector_db.add_transcription(batch, transcription_data)

    # Check if the data object is added to the batch correctly
    assert len(batch.data_objects) == 1
    assert batch.data_objects[0]["data_object"] == {
        "title": "Sample Title",
        "id_title": "sample_id",
        "text": "Sample transcription text",
        "start_time": 0.0,
        "end_time": 1.0
    }
    assert batch.data_objects[0]["class_name"] == "Transcriptions"
    assert isinstance(batch.data_objects[0]["uuid"], str)
    assert batch.data_objects[0]["vector"] == [0.1, 0.2, 0.3]

    # Check if the method returns a transcription ID
    assert isinstance(transcription_id, str)

def test_insert_to_db(vector_db):
    # Sample data for insert_to_db
    data = [
        {"title": "Title1", "id": "id1", "text": "Text1", "start": 0.1, "end": 0.5, "vector": [0.1, 0.2, 0.3]},
        {"title": "Title2", "id": "id2", "text": "Text2", "start": 0.2, "end": 0.6, "vector": [0.4, 0.5, 0.6]}
    ]

    # Call insert_to_db method
    vector_db.insert_to_db(data)

    # Check if the data objects are created in the batch
    assert len(vector_db.client.batch.data_objects) == len(data)

def test_batch_insert(vector_db):
    # Sample data for batch_insert
    data_folder = "YOUR_DATA_FOLDER_PATH_HERE"
    vector_db.get_file_paths(data_folder)

    # Call batch_insert method
    vector_db.batch_insert(embedding_api="http://example.com")

    # Check if the data objects are created in the batch
    assert len(vector_db.client.batch.data_objects) == 2

    # Check if the references are created in the batch
    assert len(vector_db.client.batch.references) == 2