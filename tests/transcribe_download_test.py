import os
import pytest
from transcription.download import * 

# Create fixtures (test data) that can be reused across multiple tests
@pytest.fixture
def example_video_url():
    return "https://www.youtube.com/watch?v=example_video_id"

@pytest.fixture
def example_playlist_url():
    return "https://www.youtube.com/playlist?list=example_playlist_id"

# Test the get_yt_data function
def test_get_yt_data(example_video_url, example_playlist_url):
    # Test with a video URL
    video_data = get_yt_data(example_video_url)
    assert isinstance(video_data, list)
    assert len(video_data) == 1
    assert "title" in video_data[0]
    assert "description" in video_data[0]
    assert "url" in video_data[0]

    # Test with a playlist URL
    playlist_data = get_yt_data(example_playlist_url)
    assert isinstance(playlist_data, list)
    assert len(playlist_data) > 0
    for item in playlist_data:
        assert "title" in item
        assert "description" in item
        assert "url" in item

# Test the download_yt_playlist function
def test_download_yt_playlist(example_video_url, tmpdir):
    video_data = [{"url": example_video_url, "title": "example_title"}]
    download_yt_playlist(video_data, str(tmpdir))
    file_location = os.path.join(str(tmpdir), "example_title.mp3")
    assert os.path.exists(file_location)

# Test the get_yt_thumbnail_link function
def test_get_yt_thumbnail_link():
    video_data = [{"url": "https://www.youtube.com/watch?v=Z56Jmr9Z34Q", "title": "example_title"}]
    result = get_yt_thumbnail_link(video_data)
    assert "thumbnail" in result[0]
    assert result[0]["thumbnail"] == "https://i.ytimg.com/vi/Z56Jmr9Z34Q/maxresdefault.jpg"

# Test the download_yt_thumbnail function
def test_download_yt_thumbnail(tmpdir):
    video_data = [{"title": "example_title", "thumbnail": "https://i.ytimg.com/vi/Z56Jmr9Z34Q/maxresdefault.jpg"}]
    download_yt_thumbnail(video_data, str(tmpdir))
    file_location = os.path.join(str(tmpdir), "example_title.jpg")
    assert os.path.exists(file_location)

