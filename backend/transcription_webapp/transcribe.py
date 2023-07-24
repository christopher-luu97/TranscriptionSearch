import os
import numpy as np
import ffmpeg
import torch
from django.db.models.query import QuerySet
import whisperx
from asgiref.sync import sync_to_async
from io import BytesIO
import asyncio
from django.http import request
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile



from .serializers import MediaFileSerializer
from .models import File

class Transcribe:
    def __init__(self):
        self.init_model_params()
        self.batch_size = 8
    
    def init_model_params(self):
        """
        Generate the model params here

        Returns:
            _type_: _description_
        """
        self.__set_device()
        device = self.device
        compute_type = "int8" # change to "int8" if low on GPU mem (may reduce accuracy)
        self.model = whisperx.load_model("medium.en", device, compute_type=compute_type)
    
    def __set_device(self):
        """
        Checks if device is CPU or GPU and then sets it
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.device = 'cpu'

    async def load_audio(self, file_data):
        """
        Convert file data to audio waveform

        Parameters
        ----------
        file_data: bytes
            The file data as bytes

        Returns
        -------
        A NumPy array containing the audio waveform, in float32 dtype.
        """
        print(f"\nFILEDATA: {file_data}\n")
        try:
            # Decode audio while down-mixing and resampling as necessary
            out, _ = (
                ffmpeg.input(file_data, threads=0)
                .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=16000)
                .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e
            # Convert the output to a NumPy array
        audio_data = np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

        return audio_data


    async def get_file_by_id(self, file_id):
        return await sync_to_async(File.objects.get)(id=file_id)
    
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


    async def _create_hms_time(self, segments):
        """
        Create new datetime values that abstract away from ever increasing seconds.
        Output is now of HH:MM:SS
        Returns:
            new_segments (list): Updated whisper results with new column
        """
        for item in segments:
            item['start_time_hms'] = self._seconds_to_time(item['start'])
            item['end_time_hms'] = self._seconds_to_time(item['end'])
        return segments

    async def transcribe_file(self, file):
        model = self.model
        device = self.device
        path = default_storage.path(file.name)

        audio_file = await self.load_audio(path)
        transcription = model.transcribe(audio_file, batch_size=self.batch_size)

        # Align model for better timestamp accuracy
        model_a, metadata = await sync_to_async(whisperx.load_align_model)(language_code=transcription["language"], device=device)
        transcription = await sync_to_async(whisperx.align)(transcription["segments"], model_a, metadata,
                                    audio_file, device, return_char_alignments=False)
        result = transcription
        text_info = []
        for txt in result['segments']:
            text_info.append(txt['text'])
        result_text = ''.join(text_info).strip(" ")
        output = await self._create_hms_time(result['segments'])
        return output


    
