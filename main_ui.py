from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLCDNumber
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
        self.record_button.clicked.connect(self.clickedrecordBtn)
        self.stop_button.clicked.connect(self.clickedstopBtn)
        self.save_button.clicked.connect(self.clickedsaveBtn)

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
        self.setWindowOpacity(0.5) # make window transparent during recording

    def clickedstopBtn(self):
        self.flag = False
        self.setWindowOpacity(1.0) # make window visible again after recording

    def clickedsaveBtn(self):
        self.flag = False
        self.setWindowOpacity(1.0) # make window visible again after recording
        self.count = 0
        self.timer_label.display(self.count)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI()
    app.exec_()
