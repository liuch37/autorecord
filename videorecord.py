"""
Create one thread for screen shot recording.
"""
import threading
import cv2
import numpy as np
import pyautogui as pg


class ScreenRecorder:
    def __init__(self, output_name, fps):
        self.output_name = output_name
        self.screen_size = tuple(pg.size())
        self.fps = fps
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # define codec
        self.out = cv2.VideoWriter(
            self.output_name, self.fourcc, self.fps, self.screen_size
        )  # create video write object
        print("Screen size {}, fps {}".format(self.screen_size, self.fps))

    def record(self):
        # get current thread
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            # make a screenshot
            img = pg.screenshot()
            # convert to numpy array for opencv processing
            frame = np.array(img)
            # convert colors from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # write the frame
            self.out.write(frame)
        # clean up object
        self.out.release()

    def start(self):
        video_thread = threading.Thread(target=self.record)
        video_thread.start()
