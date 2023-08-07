import whisperx
import torch

class Transcriber():
    def __init__(self, device:str = "cpu", batch_size:int=4, compute_type:str="int8"):
        """
        Instantiate the class with minimal resources

        Args:
            device (str, optional): cpu or cuda. Defaults to "cpu".
            batch_size (int, optional): Bigger number requires more memory. Defaults to 4.
            compute_type (str, optional): float16 requires more memory. Defaults to "int8".
        """
        self.device = device
        self.batch_size = batch_size
        self.compute_type = compute_type

    def transcribe_file(self, audio_file:str, title:str) -> list:
        """
        Transcripe the files

        Args:
            audio_file (str): Name of the audio file
            title (str): title of the video

        Returns:
            list: _description_
        """
        device = self.device
        compute_type = self.compute_type
        batch_size = self.batch_size

        # 1. Transcribe with original whisper (batched) with medium.en for speed/accuracy tradeoff
        model = whisperx.load_model("medium.en", device, compute_type=compute_type)

        audio = whisperx.load_audio(audio_file)
        result = model.transcribe(audio, batch_size=batch_size)

        # delete model if low on GPU resources
        # import gc; gc.collect(); torch.cuda.empty_cache(); del model

        # 2. Align whisper output
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
        result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
        import gc; gc.collect(); torch.cuda.empty_cache(); del model
        counter = 0
        for r in result["segments"]:
            r['id'] = str(counter)+"_"+title
            r['title'] = title
            counter +=1

        return result

    def process_data(self, data:dict)->dict:
        """
        Process the data to a specific output format

        Args:
            data (dict): Dictionary of transcription results

        Returns:
            output (dict): Dictionary with new schema
        """
        # Extract the necessary information from the data
        title = data['title']
        url = data['file_location']

        # Call the transcribe_file function with the video URL
        result = self.transcribe_file(url, title)

        # Create a dictionary with the desired output format
        output = {
            'title': title,
            'segments': result["segments"]
        }

        return output