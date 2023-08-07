from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
import asyncio
import os
from django.shortcuts import render
import json
from .query_vector_DB import queryVectorDB

@csrf_exempt
def individual_transcription(request):
    """
    API that retrieves the individual transcfription data from a weaviate instance
    The weaviate instance is hosted in docker and should have existing schema with data

    Args:
        request (file): File object of form data

    Returns:
        JsonResponse: Formatted JsonResponse object on success
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')

            if title is not None:
                # transcriptions = get_weaviate_data(title) # [{}] format
                data = title #[{"Example key": "Example Value"}]
                vector_db_endpoint = "http://localhost:8080"
                qvb = queryVectorDB(vector_db_endpoint)
                query = title
                result = qvb.get_data_from_title(query)

                if result is not None:
                    response_data = {
                        'status': 'success',
                        'message': 'File received and processed successfully',
                        'data': result
                    }
                    return JsonResponse(response_data)
                else:
                    return HttpResponseBadRequest("Failed to GET the transcription from vector database")
            else:
                return HttpResponseBadRequest("No title received")
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON data")
    else:
        return HttpResponseBadRequest("Invalid request method")
    
@csrf_exempt
def query_all_transcription(request):
    """
    API that retrieves the all individual transcription data from a weaviate instance based on natural language query
    The weaviate instance is hosted in docker and should have existing schema with data
    Natural language query should call upon a separate docker instance to embed the query to a vector.

    Args:
        request (file): File object of form data

    Returns:
        JsonResponse: Formatted JsonResponse object on success
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query')

            if query is not None:
                # transcriptions = get_weaviate_data(title) # [{}] format
                vector_db_endpoint = "http://localhost:8080"
                embedding_api = "http://127.0.0.1:8200/embed"
                qvb = queryVectorDB(vector_db_endpoint)
                result = qvb.get_data_from_query(query, embedding_api)
                # result = [{"Title": "Yes Title", "Text":"Yes Text"},
                #           {"Title": "Yes Title 2", "Text":"Yes Text 2"},
                #           {"Title": "Yes Title 3", "Text":"Yes Text 3"},
                #           {"Title": "Yes Title 4", "Text":"Yes Text 4"},
                #           {"Title": "Yes Title 5", "Text":"Yes Text 5"},
                #           {"Title": "Yes Title 6", "Text":"Yes Text 6"},
                #           {"Title": "Yes Title 7", "Text":"Yes Text 7"},
                #           {"Title": "Yes Title 8", "Text":"Yes Text 8"},
                #           {"Title": "Yes Title 9", "Text":"Yes Text 9"},
                #           {"Title": "Yes Title 10", "Text":"Yes Text 10"},
                #           {"Title": "Yes Title 11", "Text":"Yes Text 11"}]

                if result is not None:
                    response_data = {
                        'status': 'success',
                        'message': 'File received and processed successfully',
                        'data': result
                    }
                    return JsonResponse(response_data)
                else:
                    return HttpResponseBadRequest("Failed to GET the transcription from vector database")
            else:
                return HttpResponseBadRequest("No title received")
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON data")
    else:
        return HttpResponseBadRequest("Invalid request method")