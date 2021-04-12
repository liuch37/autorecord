"""
Create one thread for audio recording.
"""
import threading
import pyaudio
import wave


def get_device_info(p, input_device_index):
    device_info = p.get_device_info_by_index(input_device_index)
    is_input = device_info["maxInputChannels"] > 0
    is_wasapi = (p.get_host_api_info_by_index(device_info["hostApi"])["name"]).find("WASAPI") != -1
    useloopback = False
    if is_input:
        print ("Selection is input using standard mode.")
    else:
        if is_wasapi:
            useloopback = True
            print ("Selection is output. Using loopback mode.")
        else:
            print ("Selection is input and does not support loopback mode. Quitting.")
            exit()
    channelcount = device_info["maxInputChannels"] if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]
    rate = int(device_info["defaultSampleRate"])

    return channelcount, rate, useloopback

class AudioRecorder:
    # Audio class based on pyaudio and wave
    def __init__(self, output_name, input_device_index):
        self.open = True
        self.frames_per_buffer = 1024
        self.input_device_index = input_device_index
        self.format = pyaudio.paInt16
        self.audio_filename = output_name
        self.audio = pyaudio.PyAudio()
        self.channels, self.rate, self.useloopback = get_device_info(self.audio, self.input_device_index)

        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            input_device_index = self.input_device_index,
            frames_per_buffer=self.frames_per_buffer,
            as_loopback = self.useloopback,
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
