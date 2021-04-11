"""
This code is the main function to record desktop screenshot and save it as a video.
"""
import cv2
import numpy as np
import pyautogui as pg
import pdb


def main():
    # get primary monitor screen size
    SCREEN_SIZE = tuple(pg.size())
    # frame per second
    FPS = 6.0
    # output video name and type
    output_name = "output.avi"
    # define codec
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    # create the video write object
    out = cv2.VideoWriter(output_name, fourcc, FPS, SCREEN_SIZE)
    print("Screen size:", SCREEN_SIZE)
    print("Start recording......")
    while True:
        try:
            # make a screenshot
            img = pg.screenshot()
            # convert these pixels to a proper numpy array to work with OpenCV
            frame = np.array(img)
            # convert colors from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # write the frame
            out.write(frame)
        except KeyboardInterrupt:
            print("Stop recording......")
            break

    # make sure everything is closed when exited
    out.release()


if __name__ == "__main__":
    main()
