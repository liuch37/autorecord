"""
This code is the main function to record desktop screenshot and save it as a video.
"""
import cv2
import numpy as np
import pyautogui as pg
import subprocess
import threading
import msvcrt
import math
from pydub import AudioSegment
from videorecord import ScreenRecorder
from audiorecord import AudioRecorder


def timing_adjust(vrec, arec):
    timing_adjustment = vrec.elapsed_time - arec.elapsed_time
    if timing_adjustment < 0:
        print(
            "WARNING: Your recorded audio time is shorter than video time."
        )
        return 0
    else:
        print("Adjust timing of audio by delaying (s)", timing_adjustment)
        return timing_adjustment


def insert_silent(timing_adjustment, aoutput_name):
    # apply audio delay
    # create silent audio segment
    silent_segment = AudioSegment.silent(
        duration=math.ceil(timing_adjustment * 1000)
    )  # duration in milliseconds
    # read wav file to an audio segment
    audio_segment = AudioSegment.from_wav(aoutput_name)
    # add above two audio segments
    delay_segment = silent_segment + audio_segment
    # save modified audio
    delay_segment.export(aoutput_name, format="wav")


def video_audio_merge(moutput_name, aoutput_name, voutput_name):
    # cmd line
    cmd = "ffmpeg.exe -y -i " + aoutput_name + " -i " + voutput_name + " -pix_fmt yuv420p " + moutput_name
    subprocess.call(cmd, shell=True)

def main():
    # frame per second
    FPS = 3.0
    # output video name and type
    voutput_name = "output.mp4"
    # output audio name and type
    aoutput_name = "audio.wav"
    # select audio device index
    device_index = 5  # default select device name: 'Speakers (Conexant ISST Audio)'
    # merge video + audio name and type
    moutput_name = "merge.mp4"
    # create screen recorder object
    vrec = ScreenRecorder(output_name=voutput_name, fps=FPS)
    # create audio recorder object
    arec = AudioRecorder(
        output_name=aoutput_name, input_device_index=device_index, fps=FPS
    )
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
            timing_adjustment = timing_adjust(vrec, arec)
            insert_silent(timing_adjustment, aoutput_name)
            print("Merge video and audio......")
            video_audio_merge(moutput_name, aoutput_name, voutput_name)
            break


if __name__ == "__main__":
    main()
