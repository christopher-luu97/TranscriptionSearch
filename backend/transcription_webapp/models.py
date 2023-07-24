from django.db import models
from django import forms
from django.core.validators import FileExtensionValidator
import datetime

from .utils.read_formats import ReadFormatsJSON

def unique_filename(_, filename):
    name, ext = filename.split('.')
    filename = f'{name}.{ext}'
    return filename

class File(models.Model):
    formats = ReadFormatsJSON()
    allowed_formats = formats.formats
    title = models.CharField(max_length=255)
    transcript = models.TextField(blank=True, null=True)
    file = models.FileField(validators=[FileExtensionValidator(allowed_extensions=allowed_formats)], upload_to=unique_filename)