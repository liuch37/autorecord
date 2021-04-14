from main import timing_adjust, insert_silent, video_audio_merge, video_convert

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLCDNumber, QDoubleSpinBox, QSpinBox
from PyQt5.QtCore import QTimer
from PyQt5 import uic
import time
import sys


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
        self.record_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.save_button.setEnabled(True)

        self.components()

        self.show()

    def components(self):
        self.count = 0
        self.flag = False
        self.timer_label.display(self.count)
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(100)

    def showTime(self):
        if self.flag:
            self.count += 1
        t = self.count / 10
        self.timer_label.display(t)

    def clickedrecordBtn(self):
        self.flag = True
        self.setWindowOpacity(0.5)  # make window transparent during recording
        self.record_button.setEnabled(False) # turn off record button
        self.count = 0
        # make a new record - start video and audio recording

    def clickedstopBtn(self):
        self.flag = False
        self.setWindowOpacity(1.0)  # make window visible again after recording
        self.record_button.setEnabled(True) # turn on record button
        # stop video and audio recording

    def clickedsaveBtn(self):
        self.flag = False
        self.setWindowOpacity(1.0)  # make window visible again after recording
        self.count = 0
        self.timer_label.display(self.count)
        # merge video and audio

        # save to intended directory and input file name
        dialog = QtWidgets.QFileDialog()
        pathsave_custom = dialog.getSaveFileName(
            None, "Select destination folder and file name", "./", "mp4 files (*.mp4)"
        )[0]
        print(pathsave_custom)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI()
    app.exec_()
