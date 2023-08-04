import weaviate
import re
from typing import Dict
from .vectorize_query import *

class queryVectorDB():
    """
    Class for the vector database
    """
    def __init__(self, endpoint:str):
        self.client = self.start(endpoint)

    def start(self, endpoint:str):
        """
        Start the client

        Args:
            endpoint(str): URL endpoint for where the weaviate instance is
        
        Returns:
            weaviate.Client

        Example:
            start("http://localhost:8080")
        """
        try:
            return weaviate.Client(endpoint)
        except Exception as E:
            print(f"Input endpoint may be incorrect at endpoint: {endpoint}")
            return 
    
    def get_data_from_title(self, query:str) -> Dict:
        """
        Retrieve data from the weaviate schema based on title
        Returned data is the entire content

        Args:
            query (str): _description_

        Returns:
            Dict: _description_
        """
        client = self.client
        where_filter = {
            "path": ["title"],
            "operator": "Equal",
            "valueText": str(query)
        }

        result = (client.query.get("Transcriptions", ["title","id_title","text", "start_time","end_time",])
                                .with_where(where_filter)
                                .with_limit(2500)
                                .do())
        result = result['data']['Get']['Transcriptions']
        new_result = self._create_hms_time(result)
        return new_result
    
    ## TODO: Edit for natural language queries.
    def get_data_from_query(self, query:str, embedding_api:str) -> Dict:
        """
        Retrieve data from the weaviate schema based on input_query
        Input query is vectorized and searched through the schema

        Args:
            query (str): _description_
            embedding_api (str):

        Returns:
            Dict: _description_
        """
        client = self.client
        tolerance = 3
        query_vector = self.embed_query(query, embedding_api)
        mem_dict, mem_dict_keys, mem_match = self.get_matched_titles(query_vector)

        final_response = [] # List of dicts
        for query_title in mem_dict_keys:
            # Get data per query
            
            query_filter = {
                            "path": ["title"],
                            "operator": "Equal",
                            "valueText": str(query_title)
                            }
            all_title_hits = client.query.get(
                "Transcriptions", ["title","id_title","text", "start_time","end_time",]
            ).with_where(query_filter).with_limit(2500).do() # Additional parameters of probability returned

            list_all_title_hits = all_title_hits["data"]["Get"]["Transcriptions"]
            string_hit = mem_dict[query_title]['id_title'] # target string from result search
            result = self.extract_number_from_string(string_hit) # get the index of the hit

            # Return context around the hit and handle edge cases for index out of bounds
            if ( result-tolerance ) < 1:
                response = list_all_title_hits[:result] + list_all_title_hits[result:result+tolerance]
            elif (result+tolerance) > (len(list_all_title_hits) - 1):
                response = list_all_title_hits[result-tolerance:result] + list_all_title_hits[result:]
            else:
                response = list_all_title_hits[result-tolerance:result+tolerance]

            individual_response = {"title":"", "text":""} # To be appended to final response
            for item in response:
                # Set the title once
                if len(individual_response["title"]) < 1:
                    individual_response["title"] = item["title"]
                individual_response["text"] += " "+ item["text"]
            individual_response["text"] = individual_response["text"].strip()
            individual_response["match"] = mem_dict[item['title']]['text'].strip()
            final_response.append(individual_response)
        return final_response
    
    def _query_response(self, query_vector: list) -> list:
        """
        Query the weaviate instance and return all matches above a threshold

        Args:
            query_vector (list): Vectorized query from POST

        Returns:
            result_subset (list): List of all the hits from the vector
        """
        client = self.client

        # Get all results
        result = client.query.get(
                "Transcriptions", ["title","id_title","text", "start_time","end_time",]
            ).with_near_vector({ # takes a dictionary of the query vector
                "vector": query_vector, 
                "certainty":0.7 # Threshold
            }
            ).with_limit(250).do()
        result_subset = result["data"]["Get"]["Transcriptions"]
        return result_subset

    def get_matched_titles(self, query_vector:list)-> tuple:
        """
        From the input query, get the title of each transcript that matched

        Args:
            result_subset (list): _description_
        
        Returns:
            (mem_dict, mem_dict_keys) tuple(dict, list): mem_dict is {title:object}, mem_dict_keys is just the titles
        """
        result_subset = self._query_response(query_vector)
        mem_dict = {}
        for item in result_subset:
            if item['title'] not in mem_dict.keys():
                mem_dict[item['title']] = item
        mem_dict_keys = list(mem_dict.keys())

        match = []
        for key, value in mem_dict.items():
            new_dict = {key:value["text"]}
            match.append(new_dict)

        return (mem_dict, mem_dict_keys, match)

    def extract_number_from_string(self, input_string: str):
        """
        Given a string return some value

        Args:
            input_string (_type_): _description_

        Returns:
            _type_: _description_

        Example:

        test_strings = [
                        "443_Lecture 3: Editors (vim) (2020).mp3",
                        "4443_Lecture 3: Editors (vim) (2020).mp3",
                        "3_Lecture 3: Editors (vim) (2020).mp3",
                        "43_Lecture 3: Editors (vim) (2020).mp3"
                        ]

        for test_string in test_strings:
            result = extract_number_from_string(test_string)
            print(f"Input: {test_string}, Extracted Number: {result}")

        
        Input: 443_Lecture 3: Editors (vim) (2020).mp3, Extracted Number: 443
        Input: 4443_Lecture 3: Editors (vim) (2020).mp3, Extracted Number: 4443
        Input: 3_Lecture 3: Editors (vim) (2020).mp3, Extracted Number: 3
        Input: 43_Lecture 3: Editors (vim) (2020).mp3, Extracted Number: 43
        
        """
        pattern = r"^\d+"
        match = re.search(pattern, input_string)
        if match:
            value = match.group()
            return int(value)
        return None
    
    def embed_query(self, query:str, embedding_api:str) -> list:
        """
        Given an input query, vectorize it 

        Args:
            query (str): Input query string from POST
            embedding_api (str): 

        Returns:
            list: Vectorized query
        """
        question_obj = questionObj(query)
        query_vector = process_item(question_obj.query, embedding_api)['vector']
        return query_vector
    
    def _seconds_to_time(self, time_value):
        """
        Convert seconds to time based on a value
        Args:
            time_value (float): Time in seconds
        Returns:
            str: String formatted in HH:MM:SS
        """
        m,s = divmod(time_value, 60)
        h, m = divmod(m, 60)
        s = int(s)
        m = int(m)
        h = int(h)
        new_value = f'{h:02d}:{m:02d}:{s:02d}'
        return new_value

    def _create_hms_time(self, segments):
        """
        Create new datetime values that abstract away from ever increasing seconds.
        Output is now of HH:MM:SS
        Returns:
            new_segments (list): Updated whisper results with new column
        """
        for item in segments:
            item['start_time'] = self._seconds_to_time(item['start_time'])
            item['end_time'] = self._seconds_to_time(item['end_time'])
        return segments


# if __name__ == "__main__":
#     vector_db_endpoint = "http://localhost:8080"
#     qvb = queryVectorDB(vector_db_endpoint)
#     query = "Lecture 3_ Editors (vim) (2020)"
#     print(qvb.get_data(query))
        