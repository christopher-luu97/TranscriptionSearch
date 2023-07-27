from yt_dlp import YoutubeDL
import pytube
from typing import List, Dict
import os
import re
import requests

def get_yt_data(url_link:str) -> List[Dict]:
  """
  Given a link, generate the data for each link and yt video

  ARGS:
    url_link(str): the url link to a video or playlist

  Returns:
    video_urls(List[Dict]): List of dictionary objects that contain basic metadata on the YT video

  """
  video_urls = []
  if "playlist" in url_link: # playlists
    playlist = pytube.Playlist(url_link)
    print('Number Of Videos In playlist: %s' % len(playlist.video_urls))
    for url in playlist:
        data_object = {"title":pytube.YouTube(url).title,
                      "description":pytube.YouTube(url).description,
                       "url":url}
        video_urls.append(data_object)
    else:
      data_object = {"title":pytube.YouTube(url).title,
                      "description":pytube.YouTube(url).description,
                     "url":url}
      video_urls.append(data_object)
  return video_urls

def download_yt_playlist(video_urls:list, path:str):
  """
  Download yt videos from list of links

  ARGS:
    video_urls(list): A list containing a hsot of youtube URL links
    path (str): path to save files

  """
  for item in video_urls:
    download_yt(item["url"], item["title"], path)
    item["file_location"] = os.path.join(path, item["title"]+".mp3")

def download_yt(url:str, out_fname:str, path:str = "input"):
  """
  Download YT videos to a specific location

  ARGS:
    url(str): A youtube url to a video
    out_fname(str): The output file name
    path(str): A path to save the file to.
  """
  if not os.path.exists(path):
    print("Path does not exist")
    return
  output = os.path.join(path, out_fname) # example: path == "input"
  ydl_opts = {
      "format": "bestaudio/best",
      "postprocessors": [
          {
              "key": "FFmpegExtractAudio",
              "preferredcodec": "mp3",
              "preferredquality": "192",
          }
      ],
      "fragment_retries": 10,
      "outtmpl": output,
  }
  with YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
  
def get_yt_thumbnail_link(url_list:List[Dict]):
    """
    Download the youtube thumbnails as jpg

    Args:
        url_list (List[Dict[str]]): List of youtube video URLS contained in dictionaries
    """
    pattern = "watch\?v=(.+)" # e.g. 'https://www.youtube.com/watch?v=Z56Jmr9Z34Q'-> 'Z56Jmr9Z34Q'
    for item in url_list:
      url = item['url']
      matched_pattern = re.search(pattern, url)
      if matched_pattern:
          content = matched_pattern.group(1)
          item['thumbnail'] = "https://i.ytimg.com/vi/" + content +"/maxresdefault.jpg" # location of where yt stores thumbnails
    return url_list

def download_yt_thumbnail(url_list:List[Dict], path:str):
  """
  Downloads youtube thumbnails to a path

  Args:
      url_list (List[Dict[str]]): List of youtube data objects
      path (str): Path to save youtube thumbnails
  """
  for item in url_list:
    img_data = requests.get(item['thumbnail']).content
    with open(os.path.join(path, item['title']+'.jpg'), 'wb') as handler:
        handler.write(img_data)

