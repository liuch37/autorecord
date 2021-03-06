import cv2
import numpy as np
import pyautogui as pg
import subprocess
import threading
import math
import os
from pathlib import Path
import pyaudio
from pydub import AudioSegment
from videorecord import ScreenRecorder_QT
from audiorecord import AudioRecorder_QT

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QPushButton,
    QLCDNumber,
    QDoubleSpinBox,
    QSpinBox,
)
from PyQt5.QtCore import QTimer, QThreadPool
from PyQt5 import uic
import time
import sys


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


def time_converter(t):
    millis = int(t)
    seconds = (millis / 10) % 60
    seconds = int(seconds)
    minutes = (millis / (10 * 60)) % 60
    minutes = int(minutes)
    hours = int(millis / (10 * 60 * 60))

    return str(hours) + ":" + str(minutes) + ":" + str(seconds) + "." + str(millis % 10)

def encode_video(set_fps, recorded_fps, voutput_name):
    cmd = "ffmpeg.exe -y -r " + str(recorded_fps) + " -i " + str(voutput_name) + " -pix_fmt yuv420p -r " + str(set_fps) + " re_" + str(voutput_name)
    subprocess.call(cmd, shell=True)
    os.remove(str(voutput_name))
    os.rename("re_"+str(voutput_name), str(voutput_name))


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("recorder.ui", self)

        # find the widgets in the xml file

        self.timer_label = self.findChild(QLCDNumber, "lcdNumber")
        self.record_button = self.findChild(QPushButton, "recordpushButton")
        self.stop_button = self.findChild(QPushButton, "stoppushButton")
        self.save_button = self.findChild(QPushButton, "savepushButton")
        self.fps_spinbox = self.findChild(QDoubleSpinBox, "fpsdoubleSpinBox")
        self.index_spinbox = self.findChild(QSpinBox, "indexspinBox")
        self.record_button.clicked.connect(self.clickedrecordBtn)
        self.stop_button.clicked.connect(self.clickedstopBtn)
        self.save_button.clicked.connect(self.clickedsaveBtn)
        self.fps_spinbox.valueChanged.connect(self.valuechangefps)
        self.index_spinbox.valueChanged.connect(self.valuechangeindex)
        self.record_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.save_button.setEnabled(False)

        # temporary output video name and type
        self.voutput_name = "video.mp4"
        # temporary output audio name and type
        self.aoutput_name = "audio.wav"

        self.fps = float(self.fps_spinbox.value())
        self.device_index = int(self.index_spinbox.value())

        self.threadpool = QThreadPool()

        self.components()

        self.audio_device_show()

        self.show()

    def audio_device_show(self):
        p = pyaudio.PyAudio()
        print("Number of device: ", p.get_device_count())
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            print(
                "Index: {} has device name: {}".format(
                    device_info["index"], device_info["name"]
                )
            )

    def components(self):
        self.count = 0
        self.flag = False
        self.timer_label.display(self.count)
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(100)  # every 0.1 s

    def showTime(self):
        if self.flag:
            self.count += 1
        # t = self.count / 10
        t = time_converter(self.count)
        self.timer_label.display(t)

    def clickedrecordBtn(self):
        self.flag = True
        self.setWindowOpacity(0.5)  # make window transparent during recording
        self.record_button.setEnabled(False)  # turn off record button
        self.save_button.setEnabled(False) # turn off save button
        self.count = 0
        # make a new record - start video and audio recording
        self.threadpool.clear()
        # create screen recorder object
        self.vrec = ScreenRecorder_QT(output_name=self.voutput_name, fps=self.fps)
        # create audio recorder object
        self.arec = AudioRecorder_QT(
            output_name=self.aoutput_name,
            input_device_index=self.device_index,
            fps=self.fps,
        )
        self.threadpool.start(self.vrec)
        self.threadpool.start(self.arec)
        self.stop_button.setEnabled(True) # turn on stop button

    def clickedstopBtn(self):
        self.flag = False
        self.setWindowOpacity(1.0)  # make window visible again after recording
        # stop video and audio recording
        self.arec.quit_flag = True
        self.vrec.quit_flag = True
        self.threadpool.clear()
        self.record_button.setEnabled(True)  # turn on record button
        self.stop_button.setEnabled(False) # turn off stop button
        self.save_button.setEnabled(True) # turn on save button

    def clickedsaveBtn(self):
        self.flag = False
        self.setWindowOpacity(1.0)  # make window visible again after recording
        self.record_button.setEnabled(False)  # turn off record button
        self.stop_button.setEnabled(False) # turn off stop button
        self.save_button.setEnabled(False) # turn off save button
        self.count = 0
        self.timer_label.display(self.count)
        # save to intended directory and input file name
        dialog = QtWidgets.QFileDialog()
        pathsave_custom = dialog.getSaveFileName(
            None, "Select destination folder and file name", "./", "mp4 files (*.mp4)"
        )[0]
        # re-encode video according to measured video length
        if Path(self.voutput_name).is_file():
            encode_video(self.vrec.fps, self.vrec.recorded_fps, self.voutput_name)
        # merge video and audio
        if len(self.arec.audio_frames) != 0 and Path(self.aoutput_name).is_file() and Path(self.voutput_name).is_file():
            timing_adjustment = timing_adjust(self.vrec, self.arec)
            insert_silent(timing_adjustment, self.aoutput_name)
            print("Merge video and audio......")
            video_audio_merge(pathsave_custom, self.aoutput_name, self.voutput_name)
        elif Path(self.voutput_name).is_file():
            print("No sound recorded. Transfer video......")
            video_convert(pathsave_custom, self.voutput_name)
        else:
            print("No sound and no video recorded.")

        self.record_button.setEnabled(True)  # turn on record button
        self.stop_button.setEnabled(False) # turn off stop button
        self.save_button.setEnabled(False) # turn off save button

    def valuechangefps(self):
        self.fps = float(self.fps_spinbox.value())

    def valuechangeindex(self):
        self.device_index = int(self.index_spinbox.value())


def main():
    app = QApplication(sys.argv)
    window = UI()
    ret = app.exec_()
    sys.exit(ret)


if __name__ == "__main__":
    main()
