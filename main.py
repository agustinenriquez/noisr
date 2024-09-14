import pyaudio
import wave
from scipy.io import wavfile
import numpy as np


# List audio input devices
def list_audio_devices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        print(f"Device {i}: {device_info['name']} (Input Channels: {device_info['maxInputChannels']})")
    p.terminate()


# Function to record audio
def record_audio(duration, filename="output.wav", rate=22050, channels=1, chunk=4096, input_device_index=None):
    p = pyaudio.PyAudio()

    # Open audio stream with the specified device index
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk,
                    input_device_index=input_device_index)  # Specify input device index

    print("Recording started...")
    frames = []

    # Record audio for the given duration
    for _ in range(0, int(rate / chunk * duration)):
        try:
            data = stream.read(chunk, exception_on_overflow=False)  # Handle overflow
            frames.append(data)
        except IOError as e:
            print(f"Warning: {e}")

    print("Recording finished.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio to a .wav file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()


# Function to analyze the audio and find the loudest peak
def analyze_audio(filename, start_time, end_time):
    # Read the recorded audio file
    rate, data = wavfile.read(filename)

    # Check if the data contains valid audio
    if np.max(np.abs(data)) == 0:
        print("Warning: No valid audio signal detected.")
        return

    # Normalize data to [-1, 1]
    data = data / np.max(np.abs(data))

    total_duration = len(data) / rate
    print(f"Total audio duration: {total_duration:.2f} seconds")

    # Calculate the start and end sample indices
    start_sample = int(rate * start_time)
    end_sample = int(rate * end_time)

    if end_sample > len(data):
        end_sample = len(data)

    if start_sample < 0 or start_sample >= end_sample:
        print("Invalid time range")
        return

    # Extract the portion of the audio in the given time range
    portion = data[start_sample:end_sample]

    # If the portion is completely silent, handle the case
    if np.max(np.abs(portion)) == 0:
        print("Warning: No audio detected in the specified time range.")
        return

    # Compute the RMS value (Root Mean Square) for the audio portion
    rms = np.sqrt(np.mean(np.square(portion)))

    if rms == 0:
        print("Warning: The RMS of the audio is zero, no sound detected.")
        return

    # Convert RMS to decibels
    db_level = 20 * np.log10(rms)

    # Find the loudest peak
    peak_index = np.argmax(np.abs(portion))
    peak_time = start_time + peak_index / rate

    print(f"Loudest peak: {peak_time:.2f}s with level {db_level:.2f} dB")


if __name__ == "__main__":
    # Step 1: List available audio devices
    print("Available audio input devices:")
    list_audio_devices()

    # Step 2: Specify the device index (use the correct index based on the list)
    device_index = int(input("Enter the device index to use for recording: "))

    # Step 3: Record audio
    duration = 10  # Recording duration in seconds
    filename = "output.wav"
    record_audio(duration, filename=filename, input_device_index=device_index)

    # Step 4: Analyze the recorded audio
    start_time = 2  # Time range start in seconds
    end_time = 8    # Time range end in seconds
    analyze_audio(filename, start_time, end_time)
