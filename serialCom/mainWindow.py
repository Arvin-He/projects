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
        self.initUI()

    def initUI(self):
        recvHexEdit.textChanged.connect(self.on_showRecvHex)
        transValEdit.textChanged.connect(self.on_showTranformData)
        tightTorqueEdit.textChanged.connect(self.on_showTightTorque)
        tightAngleEdit.textChanged.connect(self.on_showTightAngle)

    def on_showRecvHex(self):
        pass

    def on_showTranformData(self):
        pass

    def on_showTightTorque(self):
        pass

    def on_showTightAngle(self):
        pass


if __name__ == "__main__":
    mainWin = MainWindow()
    mainWinRect = mainWin.geometry()
    mainWin.setFixedSize(mainWinRect.size())
    mainWin.exec_()
