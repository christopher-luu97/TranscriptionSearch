# API to handle user requesting to download files of different formatsimport os
from django.http import request
import csv
import json
from django.http import HttpResponse
import io

class Download():
    """
    This class handles the relevant downloading of files on request

    Raises:
        RuntimeError: _description_

    Returns:
        _type_: _description_
    """
    def __init__(self):
        pass

    def generate_csv(self, transcription_data):
        # Create a file-like buffer to receive CSV data
        buffer = io.StringIO()
        
        fieldnames = ['start_time', 'end_time', 'text']
        
        # Create the CSV writer
        writer = csv.DictWriter(buffer, fieldnames=fieldnames)
        
        # Write the CSV header
        writer.writeheader()
        
        # Write each segment as a CSV row
        for segment in transcription_data:
            writer.writerow({
                'start_time': segment['start_time_hms'],
                'end_time': segment['end_time_hms'],
                'text': segment['text']
            })
        
        # Get the CSV content from the buffer
        csv_content = buffer.getvalue()
        
        # Close the buffer
        buffer.close()
        
        return csv_content
    
    def generate_srt(self, transcription_data):
        buffer = io.StringIO()
        index = 1

        # Write each segment as an SRT entry
        for segment in transcription_data:
            start_time = segment['start_time_hms']
            end_time = segment['end_time_hms']
            text = segment['text']
            
            # Write the entry index
            buffer.write(str(index))
            buffer.write('\n')
            
            # Write the time range
            buffer.write(f"{start_time} --> {end_time}")
            buffer.write('\n')
            
            # Write the text
            buffer.write(text)
            buffer.write('\n\n')
            
            index += 1

        srt_content = buffer.getvalue()
        buffer.close()

        return srt_content

    def generate_vtt(self, transcription_data):
        buffer = io.StringIO()

        # Write the VTT header
        buffer.write("WEBVTT")
        buffer.write('\n\n')

        # Write each segment as a VTT cue
        for segment in transcription_data:
            start_time = segment['start_time_hms']
            end_time = segment['end_time_hms']
            text = segment['text']
            
            # Write the cue time range
            buffer.write(f"{start_time} --> {end_time}")
            buffer.write('\n')
            
            # Write the text
            buffer.write(text)
            buffer.write('\n\n')

        vtt_content = buffer.getvalue()
        buffer.close()

        return vtt_content

    def generate_txt(self, transcription_data):
        buffer = io.StringIO()

        for segment in transcription_data:
            start_time = segment['start_time_hms']
            end_time = segment['end_time_hms']
            text = segment['text']

            # Write the segment information to the buffer
            buffer.write(f"[{start_time} --> {end_time}]\n")
            buffer.write(f"{text}\n\n")

        txt_content = buffer.getvalue()
        buffer.close()

        return txt_content

    def download(self, fmat, dta, filename):
        if fmat and dta:
            # Parse the JSON data
            transcription_data = json.loads(dta)

            # Generate the file content based on the selected format
            if fmat == "csv":
                file_content = self.generate_csv(transcription_data)
                content_type = "text/csv"
                file_extension = "csv"
            elif fmat == "txt":
                file_content = self.generate_txt(transcription_data)
                content_type = "text/plain"
                file_extension = "txt"
            elif fmat == "srt":
                file_content = self.generate_srt(transcription_data)
                content_type = "application/x-subrip"
                file_extension = "srt"
            elif fmat == "vtt":
                file_content = self.generate_vtt(transcription_data)
                content_type = "text/vtt"
                file_extension = "vtt"

            # Create the file response
            response = HttpResponse(file_content, content_type=content_type)
            response["Content-Disposition"] = f"attachment; filename={filename}.{file_extension}"
            return response

        return HttpResponse(status=400)

    
