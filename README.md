# Autorecord
Automatic recording for desktop video and audio. This repo only supports Windows system - only being tested on 64-bit Windows 10.

## Install

### Create an virtual environment using conda with Python 3.7, i.e.,
```
conda create -n autorecord python=3.7
```

### Install required python library:
```
pip install -r requirements.txt
```

### Install pyaudio library:

To install pyaudio, you need to download the modified version which supports loopback feature in pyaudio, in https://github.com/intxcc/pyaudio_portaudio. There are prebuild releases for Python 3.7 where you can download here https://github.com/intxcc/pyaudio_portaudio/releases, and then do pip install, i.e.,
```
pip install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl
```
