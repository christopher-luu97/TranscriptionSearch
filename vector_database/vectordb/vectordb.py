import json
import weaviate
from weaviate.batch import Batch
from weaviate.util import generate_uuid5
from tqdm import trange
import os
from .util import *
import multiprocessing as mp
import functools
from typing import List, Dict

class vectorDB():
    """
    Class for the vector database
    """
    def __init__(self):
        self.cpu_count  = mp.cpu_count()

    def start(self, endpoint:str):
        """
        Start the client

        Args:
            endpoint(str): URL endpoint for where the weaviate instance is

        Example:
            start("http://localhost:8080")
        """
        try:
            self.client = weaviate.Client(endpoint)
        except Exception as E:
            print(f"Input endpoint may be incorrect at endpoint: {endpoint}")
            return 
    
    def check_schema(self):
        """
        Do checks on the loaded schema
        Schema can be found in schema.json
        This will do error handling and tests should be made to ensure we are expecting the right thing
        """
        pass

    def create_schema(self, schema:json):
        """
        Create schema if it does not exist
        """
        if len(self.client.schema.get()) < 1: # if does not exist
            self.client.schema.create(schema)
        else:
            print(f"Schema already exists: {self.client.get_meta()}")
            return

    def get_file_paths(self, folder_path:str):
        """
        Given an input folder path, get all the paths to individual files that have been transcribed

        Args:
            folder_path (str): _description_
        """
        self.DATA_PATH = folder_path
        self.TRANSCRIPTS = [item for item in os.listdir(folder_path) if ".json" in item]
    
    def embedding_api_url(self, embedding_api:str):
        """
        Method to store the embedding API

        Args:
            embedding_api (str): _description_
        """
        self.embedding_api = embedding_api

    def check_file_content(self):
        """
        Given all the files to be vectorized, check they follow the expected structure.
        This is required because users may edit the output from the transcription prior to this step.

        """
        pass

    def add_transcription(self, batch: Batch, transcription_data: dict) -> str:
        """
        Add the transcription objects to the scheme
        """
        # Create the transcription object
        transcription_object = {
            'title': transcription_data['title'],  # Assuming 'id' in the data corresponds to the title
            'id_title': transcription_data['id'],
            'text': transcription_data['text'],
            'start_time': transcription_data['start'],
            'end_time': transcription_data['end']
        }

        # Generate a unique UUID for the transcription
        transcription_id = generate_uuid5(transcription_data['id'])

        # Add the transcription object to the batch request
        batch.add_data_object(
            data_object=transcription_object,
            class_name='Transcriptions',
            uuid=transcription_id,
            vector=transcription_data['vector']
        )

        return transcription_id

    def insert_to_db(self, data:List[Dict]):
        """
        Insert the content to the created data objects
        """
        client = self.client
        with client.batch as batch:
            for i in trange(1, len(data)):
                item_id = self.add_transcription(batch, data[i])
                # submit the objects from the batch to weaviate
                batch.create_objects()
                # submit the reference from the batch to weaviate
                batch.create_references()

    def batch_insert(self, embedding_api:str=None):
        """
        Given a list of files, vectorize and insert them

        Args:
            embedding_api(str): URL endpoint for where the embeddign model API is
        """
        DATA_PATH = self.DATA_PATH
        TRANSCRIPTS = self.TRANSCRIPTS
        if embedding_api:
            embedding_api = embedding_api
        else:
            embedding_api = self.embedding_api
        for i in range(len(os.listdir(DATA_PATH))-1):
            print(f"\nInserting: {os.path.join(DATA_PATH, TRANSCRIPTS[i])}\n")
            with open(os.path.join(DATA_PATH, TRANSCRIPTS[i]), 'r') as f:
                content = json.load(f)
                for item in content['segments']:
                    item['title'] = TRANSCRIPTS[i][:-9] # always remove ".mp3.json" which has length of 9 from string
            
                num_processes = self.cpu_count
                args_list = [(embedding_api, segment, headers) for segment in content['segments']]
                with mp.Pool(processes=num_processes) as pool:
                    updated_content = pool.map(process_item, args_list)
                
                self.insert_to_db(updated_content) 
        print("Schema inserted!")

