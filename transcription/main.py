import os
import json

from download import *
from transcribe import Transcriber

def main(folder_path:str, transcriber: object):
    """
    Transcribe a list of files

    Args:
        folder_path (str): folder path to where the downloaded videos are
        transcriber (object): take in the transcriber object
    """
    file_paths = []
    for data in os.listdir(folder_path):
        data_ob = {"title":data[:-4], "file_location":os.path.join(folder_path,data)}
        file_paths.append(data_ob)

    for item in file_paths:
        if ".mp3" in item['file_location']: # Basic check for now.
            result = transcriber.process_data(item)
            with open(os.path.join(folder_path, item['title']+".json", 'w')) as fp:
                json.dump(result, fp)

if __name__ == "__main__":
    device = "cpu"  # "cuda"
    batch_size = 4 # reduce if low on GPU mem e.g. 16
    compute_type = "int8" # change to "int8" if low on GPU mem (may reduce accuracy)
    transcriber = Transcriber(device, batch_size, compute_type)

    url_link = input("Youtube URL: ") # e.g. "https://www.youtube.com/playlist?list=PLyzOVJj3bHQuloKGG59rS43e29ro7I57J"
    data_list = get_yt_data(url_link)
    print(f"\nThere are {len(data_list)} number of videos in the provided link\n")
    output_path = input("Output folder: ")
    download_yt_playlist(data_list, output_path)
    print(f"\nFiles downloaded to {output_path} with {len(os.listdir(output_path))} files.\n")

    new_data_list = get_yt_thumbnail_link(data_list)
    download_yt_thumbnail(new_data_list, output_path)

    main(output_path, transcriber)
    print(f"\nExecution success! Transcriptions are at {output_path}\n")


