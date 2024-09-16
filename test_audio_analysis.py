import pytest
import numpy as np
from scipy.io import wavfile
from unittest.mock import patch
from main import analyze_audio

@pytest.fixture
def setup_audio_file(tmpdir):
    wav_file_path = tmpdir.join("test_output.wav")
    sample_rate = 44100
    duration = 5
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio_data = 0.5 * np.sin(2 * np.pi * 440 * t)
    wav_file_path_str = str(wav_file_path)
    wavfile.write(wav_file_path_str, sample_rate, audio_data.astype(np.float32))
    return wav_file_path_str

def test_analyze_audio_loudest_peak(setup_audio_file):
    filename = str(setup_audio_file)
    with patch('main.wavfile.read') as mock_read:
        mock_read.return_value = (44100, np.sin(np.linspace(0, 10, 44100 * 10)))
        result = analyze_audio(filename, start_time=2, end_time=8)
        assert result is None

def test_analyze_audio_silent_file():
    silent_data = np.zeros(44100 * 5)
    with patch('main.wavfile.read', return_value=(44100, silent_data)):
        result = analyze_audio("silent.wav", start_time=0, end_time=5)
        assert result is None
