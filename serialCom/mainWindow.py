# usr/bin/python3
# -*- coding:utf-8 -*-

import sys
import os
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog

app = QtWidgets.QApplication(sys.argv)


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "res/serialCom.ui"), self)
        # self.initUI()

    def initUI(self):
        self.setGeometry(300, 150, 600, 600)
        self.setWindowTitle("Value Reader")
        self.show()


if __name__ == "__main__":
    mainWin = MainWindow()
    mainWinRect = mainWin.geometry()
    mainWin.setFixedSize(mainWinRect.size())
    mainWin.exec_()
