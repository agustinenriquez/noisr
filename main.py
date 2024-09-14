import pyaudio
import wave
from scipy.io import wavfile
import numpy as np


def record_audio(duration, filename="output.wav", rate=44100, channels=1, chunk=1024):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Recording started...")
    frames = []

    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to find the peak noise level in a time range
def analyze_audio(filename, start_time, end_time):
    rate, data = wavfile.read(filename)
    data = data / np.max(np.abs(data))  # Normalize data to [-1, 1]
    
    total_duration = len(data) / rate
    print(f"Total audio duration: {total_duration:.2f} seconds")
    
    start_sample = int(rate * start_time)
    end_sample = int(rate * end_time)

    if end_sample > len(data):
        end_sample = len(data)
    
    if start_sample < 0 or start_sample >= end_sample:
        print("Invalid time range")
        return

    portion = data[start_sample:end_sample]
    
    rms = np.sqrt(np.mean(np.square(portion)))  # Root Mean Square
    db_level = 20 * np.log10(rms)

    peak_index = np.argmax(np.abs(portion))
    peak_time = start_time + peak_index / rate

    print(f"Loudest peak: {peak_time:.2f}s with level {db_level:.2f} dB")


if __name__ == "__main__":
    duration = 10  # Recording duration in seconds
    start_time = 2  # Time range start in seconds
    end_time = 8    # Time range end in seconds

    record_audio(duration, filename="output.wav")
    analyze_audio("output.wav", start_time
