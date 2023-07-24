from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from transcription_webapp.models import File

from .utils.read_formats import ReadFormatsJSON


class MediaFileSerializer(serializers.Serializer):
    # This does not validate the content of the data itself, just the extension!
    formats = ReadFormatsJSON()
    allowed_formats = formats.formats
    audio_file = serializers.FileField(
        validators=[FileExtensionValidator(allowed_extensions=allowed_formats)])

    class Meta:
        model = File
        fields = ('id', 'title', 'transcript', 'file')