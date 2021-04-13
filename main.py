"""
This code is the main function to record desktop screenshot and save it as a video.
"""
import cv2
import numpy as np
import pyautogui as pg
import ffmpeg
import threading
import msvcrt
from pydub import AudioSegment
from videorecord import ScreenRecorder
from audiorecord import AudioRecorder


def main():
    # frame per second
    FPS = 3.0
    # output video name and type
    voutput_name = "output.mp4"
    # output audio name and type
    aoutput_name = "audio.wav"
    # select audio device index
    device_index = 5  # default select device name: 'Speakers (Conexant ISST Audio)'
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
            break
    print("Merge video and audio......")
    timing_adjustment = vrec.elapsed_time - arec.elapsed_time
    if timing_adjustment < 0:
        print(
            "WARNING: Your recorded audio time is shorter than video time, which should not be correct. Check your frame rate for video."
        )
    else:
        print("Adjust timing of audio by delaying (s)", timing_adjustment)
    # apply audio delay
    # create silent audio segment
    silent_segment = AudioSegment.silent(
        duration=int(timing_adjustment * 1000)
    )  # duration in milliseconds
    # read wav file to an audio segment
    audio_segment = AudioSegment.from_wav(aoutput_name)
    # add above two audio segments
    delay_segment = silent_segment + audio_segment
    # save modified audio
    delay_segment.export(aoutput_name, format="wav")

    # merge audio and video
    input_video = ffmpeg.input(voutput_name)
    input_audio = ffmpeg.input(aoutput_name)
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output("merge.mp4").run()
    # cmd line
    # cmd = "ffmpeg -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video.avi -pix_fmt yuv420p " + filename + ".avi"
    # subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    main()
