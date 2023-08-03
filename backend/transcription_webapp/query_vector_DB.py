import weaviate
from typing import Dict

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
    def get_data_from_query(self, query:str) -> Dict:
        """
        Retrieve data from the weaviate schema based on input_query
        Input query is vectorized and searched through the schema

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
        