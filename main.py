"""
This code is the main function to record desktop screenshot and save it as a video.
"""
import cv2
import numpy as np
import pyautogui as pg
import ffmpeg
import threading
import msvcrt
from videorecord import ScreenRecorder
from audiorecord import AudioRecorder


def main():
    # frame per second
    FPS = 6.0
    # output video name and type
    voutput_name = "output.mp4"
    # output audio name and type
    aoutput_name = "audio.wav"
    # select audio device index
    device_index = 5  # default select device name: 'Speakers (Conexant ISST Audio)'
    # create screen recorder object
    vrec = ScreenRecorder(output_name=voutput_name, fps=FPS)
    # create audio recorder object
    arec = AudioRecorder(output_name=aoutput_name, input_device_index=device_index)
    # create video thread and start recording
    print("Start recording......")
    vrec.start()
    arec.start()
    while True:
        # catch keyboard key 'q' to stop recording
        if msvcrt.kbhit() and msvcrt.getch() == b"q":
            print("Stop recording......")
            vrec.stop()
            arec.stop()
            break
    print("Merge video and audio......")
    input_video = ffmpeg.input(voutput_name)
    input_audio = ffmpeg.input(aoutput_name)
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output('merge.mp4').run()


if __name__ == "__main__":
    main()
