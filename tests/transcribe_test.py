import pytest
from unittest.mock import Mock, patch
from transcription.transcribe import Transcriber

# Create fixtures (test data) that can be reused across multiple tests
@pytest.fixture
def transcriber():
    return Transcriber()

@pytest.fixture
def mock_whisperx():
    # Mock the whisperx.load_model function
    mock_model = Mock()
    mock_model.transcribe.return_value = {"segments": [{"text": "Mocked transcription"}]}
    return mock_model

@pytest.fixture
def mock_whisperx_align_model():
    # Mock the whisperx.load_align_model function
    mock_align_model = Mock()
    mock_align_model.transcribe.return_value = {"segments": [{"text": "Mocked aligned transcription"}]}
    return mock_align_model

# Test the transcribe_file function
def test_transcribe_file(transcriber, mock_whisperx):
    audio_file = "example_audio.wav"
    title = "Example Title"

    # Patch the whisperx.load_model function to use the mock model
    with patch("whisperx.load_model", return_value=mock_whisperx):
        result = transcriber.transcribe_file(audio_file, title)

    assert "segments" in result
    assert len(result["segments"]) > 0
    assert result["segments"][0]["text"] == "Mocked transcription"

# Test the process_data function
def test_process_data(transcriber, mock_whisperx, mock_whisperx_align_model):
    data = {
        "title": "Example Title",
        "file_location": "example_audio.wav"
    }

    # Patch the whisperx.load_model and whisperx.load_align_model functions
    # to use the mock models
    with patch("whisperx.load_model", return_value=mock_whisperx), \
         patch("whisperx.load_align_model", return_value=mock_whisperx_align_model):
        result = transcriber.process_data(data)

    assert "title" in result
    assert "segments" in result
    assert len(result["segments"]) > 0
    assert result["segments"][0]["text"] == "Mocked aligned transcription"
    assert result["title"] == "Example Title"
