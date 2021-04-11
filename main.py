"""
This code is the main function to record desktop screenshot and save it as a video.
"""
import cv2
import numpy as np
import pyautogui as pg
import threading
import msvcrt
from videorecord import ScreenRecorder


def main():
    # frame per second
    FPS = 6.0
    # output video name and type
    output_name = "output.mp4"
    # create screen recorder object
    rec = ScreenRecorder(output_name=output_name, fps=FPS)
    # create video thread and start recording
    video_thread = threading.Thread(target=rec.record)
    video_thread.start()
    print("Start recording......")
    while True:
        # catch keyboard key 'q' to stop recording
        if msvcrt.kbhit() and msvcrt.getch() == b"q":
            print("Stop recording......")
            video_thread.do_run = False
            break


if __name__ == "__main__":
    main()
