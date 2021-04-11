# Autorecord
Automatic recording for desktop video and audio. This repo only supports Windows system - only being tested on 64-bit Windows 10.

## Install
Create an virtual environment using conda, e.g., 
```
conda create -n autorecord python=3.7
```

Install required python library:
```
pip install -r requirements.txt
```

Note to install pyaudio package, you need to download the correct wheel https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio and then do pip install, e.g.,
```
pip install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl
```
