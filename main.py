'''
This code is the main function to record desktop screenshot and save it as a video.
'''
import cv2
import numpy as np
import pyautogui as pg
import pdb

def main():
    # get primary monitor screen size
    img = pg.screenshot()
    # convert these pixels to a proper numpy array to work with OpenCV
    frame = np.array(img)
    Height, Width, _ = frame.shape
    SCREEN_SIZE = (Width, Height)
    # frame per second
    FPS = 10.0
    # output video name and type
    output_name = "output.avi"
    # define codec
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    # create the video write object
    out = cv2.VideoWriter(output_name, fourcc, FPS, SCREEN_SIZE)
    print(SCREEN_SIZE)

    while True:
        # make a screenshot
        img = pg.screenshot()
        # convert these pixels to a proper numpy array to work with OpenCV
        frame = np.array(img)
        # convert colors from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # write the frame
        out.write(frame)
        # show the frame
        cv2.imshow("screenshot", frame)
        # if the user clicks q, it exits
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # make sure everything is closed when exited
    cv2.destroyAllWindows()
    out.release()

if __name__ == "__main__":
    main()