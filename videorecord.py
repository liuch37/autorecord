"""
Create one thread for screen shot recording.
"""
import threading
import cv2
import numpy as np
import pyautogui as pg
import time
from PyQt5.QtCore import QThread


class ScreenRecorder:
    def __init__(self, output_name, fps):
        self.open = True
        self.output_name = output_name
        self.screen_size = tuple(pg.size())
        self.fps = fps
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # define codec
        self.out = cv2.VideoWriter(
            self.output_name, self.fourcc, self.fps, self.screen_size
        )  # create video write object
        print("Screen size {}, fps {}".format(self.screen_size, self.fps))
        self.frame_counts = 1
        self.start_time = time.time()
        self.elapsed_time = time.time()

    def record(self):
        flag = True
        while self.open == True:
            # make a screenshot
            img = pg.screenshot()
            # convert to numpy array for opencv processing
            frame = np.array(img)
            # convert colors from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # above image processing delay ~ 0.25 s
            # write the frame
            self.out.write(frame)
            if flag:
                self.start_time = time.time()
                flag = False
            self.frame_counts += 1

    def start(self):
        video_thread = threading.Thread(target=self.record)
        video_thread.start()

    def stop(self):
        if self.open == True:
            self.open = False
            # clean up object
            self.out.release()
            self.elapsed_time = time.time() - self.start_time
            frame_counts = self.frame_counts
            recorded_fps = frame_counts / self.elapsed_time
            print("Total video frames " + str(frame_counts))
            print("Video elapsed time " + str(self.elapsed_time))
            print("Video recorded fps " + str(recorded_fps))
        else:
            pass


class ScreenRecorder_QT(QThread):
    def __init__(self, output_name, fps):
        super(ScreenRecorder_QT, self).__init__()
        self.quit_flag = False
        self.output_name = output_name
        # self.screen_size = tuple(pg.size())
        self.screen_size = tuple((512, 512))
        self.fps = fps
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # define codec
        self.out = cv2.VideoWriter(
            self.output_name, self.fourcc, self.fps, self.screen_size
        )  # create video write object
        print("Screen size {}, fps {}".format(self.screen_size, self.fps))
        self.frame_counts = 1
        self.start_time = time.time()
        self.elapsed_time = time.time()

    def run(self):
        while True:
            if not self.quit_flag:
                self.record()
            else:
                break

        self.quit()

    def record(self):
        # make a screenshot
        # img = pg.screenshot()
        time.sleep(0.1)  # create simulated 0.1 sec delay
        # convert to numpy array for opencv processing
        # frame = np.array(img)
        frame = np.random.randint(0, 256, (512, 512, 3), dtype="uint8")
        # convert colors from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # above image processing delay ~ 0.25 s
        # write the frame
        self.out.write(frame)
        self.frame_counts += 1

    def stop(self):
        self.quit_flag = True
        self.out.release()
        self.elapsed_time = time.time() - self.start_time
        frame_counts = self.frame_counts
        recorded_fps = frame_counts / self.elapsed_time
        print("Total video frames " + str(frame_counts))
        print("Video elapsed time " + str(self.elapsed_time))
        print("Video recorded fps " + str(recorded_fps))
