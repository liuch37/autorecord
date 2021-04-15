# Autorecord
Automatic recording for primary monitor screenshot video and its audio - for online meeting recording application. This software only supports Windows system - only being tested on 64-bit Windows 10.

## Install

### Create an virtual environment using conda with Python 3.7
```
conda create -n autorecord python=3.7
```

### Install required python library
```
pip install -r requirements.txt
```

### Install pyaudio library

To install pyaudio, you need to download the modified version which supports loopback feature in pyaudio, in https://github.com/intxcc/pyaudio_portaudio. There are prebuild releases for Python 3.7 where you can download here https://github.com/intxcc/pyaudio_portaudio/releases, and then do pip install, i.e.,
```
pip install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl
```

### (Optional) ffmpeg

We have provided the ffmpeg.exe in this repository and we will use it directly in the code. No need to install yourself. But you may install and use your own ffmpeg, this would require minor changes in the code.

## How to Start Recording

### Step 1: Device Inspection
Run the below script to find the proper device index for the audio device that can be supported using loopback.

```
python device_inspection.py
```

### Step 2: Screenshot video Record

Simply run the below command:

```
python main.py --fps 3.0 --output record.mp4 --index 5
```

--fps: Frame per second for the recorded video. The default is set to 3.0.

--output: Output name for the final video being saved. The default is set to 'record.mp4'.

--index: Proper audio device index found in the first step. Try to find device index with name 'Speakers (Conexant ISST Audio)' if you want to record system sound coming out from default speaker.

### How to Stop Recording

Simply press 'q' on your terminal to stop and save your recording. This program will save 'video.mp4', 'audio.wav', and 'record.mp4' as video only, audio ony, and merged video with audio, respectively, as three output files.

### How to Run PyQT Version

Simply run the below command to launch PyQT interface and start using this app. You can record, stop, and save. Note that please save your final output file within the same script folder. Each time you click `record` is a new recording.
```
python main_ui.py
```

### How to Install PyQT Version as a Windows App

Run the below command and you will get both `build` and `dist` folders. Remember to also put `ffmpeg.exe` and `recorder.ui` in `dist` folder in order to run .exe file.
```
pyinstaller main_ui.py --onefile --name AutoRecorder
```
