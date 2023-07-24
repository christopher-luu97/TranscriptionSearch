from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .transcribe import Transcribe
from .download import Download
from rest_framework import viewsets
from .models import File
from .serializers import MediaFileSerializer
import asyncio
import os

@csrf_exempt
def transcribe(request):
    """
    API to handle transcription service

    Args:
        request (file): File object of form data

    Returns:
        JsonResponse: Formatted JsonResponse object on success
    """
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        transcriber = Transcribe()

        # Save the file to the storage and get its ID
        file_instance = File(file=file)
        file_instance.save()
        file_id = file_instance.id

        data = file_instance
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(transcriber.transcribe_file(file))

        # Delete the uploaded media file
        file_path = file_instance.file.path
        os.remove(file_path)
        
        if data is not None:
            response_data = {
                'status': 'success',
                'message': 'File received and processed successfully',
                'data': data
            }
            return JsonResponse(response_data)
        else:
            return HttpResponseBadRequest("Failed to transcribe the file")
    else:
        return HttpResponseBadRequest("No file received")

@csrf_exempt
def download(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        fmat = request.POST.get('format')
        filename = request.POST.get('file_name')
        downloader = Download()
        response = downloader.download(fmat, data, filename)
        return response
    else:
        return HttpResponseBadRequest("No file received")


class FileView(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = MediaFileSerializer