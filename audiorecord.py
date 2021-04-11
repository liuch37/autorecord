"""
Create one thread for audio recording.
"""
import threading
import pyaudio
import wave


class AudioRecorder:
    # Audio class based on pyaudio and wave
    def __init__(self, output_name, rate):
        self.open = True
        self.rate = rate
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        self.audio_filename = output_name
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            input_device_index = 1,
            frames_per_buffer=self.frames_per_buffer,
        )
        self.audio_frames = []

    # Audio starts being recorded
    def record(self):
        self.stream.start_stream()
        while self.open == True:
            data = self.stream.read(self.frames_per_buffer)
            self.audio_frames.append(data)
            if self.open == False:
                break

    # Finishes the audio recording therefore the thread too
    def stop(self):
        if self.open == True:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

            waveFile = wave.open(self.audio_filename, "wb")
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b"".join(self.audio_frames))
            waveFile.close()
        else:
            pass

    # Launches the audio recording function using a thread
    def start(self):
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()
