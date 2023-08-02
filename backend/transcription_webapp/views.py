from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import File
from .serializers import MediaFileSerializer
import asyncio
import os
from django.shortcuts import render
import json
from .query_vector_DB import queryVectorDB

def index(request):
    return render(request, 'index.html')

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
                result = qvb.get_data(query)
                print(result[0])

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


class FileView(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = MediaFileSerializer