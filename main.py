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
import os
from pathlib import Path
import pyaudio
import argparse
from pydub import AudioSegment
from videorecord import ScreenRecorder
from audiorecord import AudioRecorder


def timing_adjust(vrec, arec):
    timing_adjustment = vrec.elapsed_time - arec.elapsed_time
    if timing_adjustment < 0:
        print("WARNING: Your recorded audio time is shorter than video time.")
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
    cmd = (
        "ffmpeg.exe -y -i "
        + aoutput_name
        + " -i "
        + voutput_name
        + " -pix_fmt yuv420p "
        + moutput_name
    )
    subprocess.call(cmd, shell=True)


def video_convert(moutput_name, voutput_name):
    # cmd line
    cmd = "ffmpeg.exe -y -i " + voutput_name + " -pix_fmt yuv420p " + moutput_name
    subprocess.call(cmd, shell=True)


def encode_video(set_fps, recorded_fps, voutput_name):
    cmd = "ffmpeg.exe -y -r " + str(recorded_fps) + " -i " + str(voutput_name) + " -pix_fmt yuv420p -r " + str(set_fps) + " re_" + str(voutput_name)
    subprocess.call(cmd, shell=True)
    os.remove(str(voutput_name))
    os.rename("re_"+str(voutput_name), str(voutput_name))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fps", type=float, default=3.0, help="frame per second for video recording"
    )
    parser.add_argument(
        "--output", type=str, default="record.mp4", help="recorded video name and type"
    )
    parser.add_argument(
        "--index", type=int, default=5, help="device index being recorded for audio"
    )

    opt = parser.parse_args()
    print(opt)
    # frame per second
    FPS = opt.fps
    # temporary output video name and type
    voutput_name = "video.mp4"
    # temporary output audio name and type
    aoutput_name = "audio.wav"
    # select audio device index
    device_index = (
        opt.index
    )  # default select device name: 'Speakers (Conexant ISST Audio)'
    # merge video + audio name and type
    moutput_name = opt.output
    # create screen recorder object
    vrec = ScreenRecorder(output_name=voutput_name, fps=FPS)
    # create audio recorder object
    arec = AudioRecorder(
        output_name=aoutput_name, input_device_index=device_index, fps=FPS
    )
    # start recording with both video and audio threads
    print("Start recording......")
    vrec.start()
    arec.start()
    while True:
        # catch keyboard key 'q' to stop recording
        if msvcrt.kbhit() and msvcrt.getch() == b"q":
            print("Stop recording......")
            vrec.stop()
            arec.stop()
            # re-encode video according to measured video length
            if Path(voutput_name).is_file():
                encode_video(vrec.fps, vrec.recorded_fps, voutput_name)
            # merge video and audio
            if len(arec.audio_frames) != 0 and Path(aoutput_name).is_file() and Path(voutput_name).is_file():
                timing_adjustment = timing_adjust(vrec, arec)
                insert_silent(timing_adjustment, aoutput_name)
                print("Merge video and audio......")
                video_audio_merge(pathsave_custom, aoutput_name, voutput_name)
            elif Path(voutput_name).is_file():
                print("No sound recorded. Transfer video......")
                video_convert(pathsave_custom, voutput_name)
            else:
                print("No sound and no video recorded.")
            break


if __name__ == "__main__":
    main()
