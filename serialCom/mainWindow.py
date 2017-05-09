# usr/bin/python3
# -*- coding:utf-8 -*-

import sys
import os
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog

import utils
import serialCommunication as serCom

app = QtWidgets.QApplication(sys.argv)


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "res/serialCom.ui"), self)
        self.initUI()

    def initUI(self):
        self.port = utils.read_config(os.path.abspath("config.ini"), "serial", "port")
        self.baud_rate = utils.read_config(os.path.abspath("config.ini"), "serial", "baudrate")
        self.portEdit.setText(self.port)
        self.baudrateEdit.setText(self.baud_rate)
        self.openBtn.clicked.connect(self.on_openCom)
        self.closeBtn.clicked.connect(self.on_closeCom)
        self.portEdit.editingFinished.connect(self.on_EditPortName)
        self.baudrateEdit.editingFinished.connect(self.on_EditBaudrate)
        self.recvHexEdit.textChanged.connect(self.on_showRecvHex)
        self.transValEdit.textChanged.connect(self.on_showTranformData)
        self.tightTorqueEdit.textChanged.connect(self.on_showTightTorque)
        self.tightAngleEdit.textChanged.connect(self.on_showTightAngle)

    def on_EditPortName(self):
        self.port = self.portEdit.text()
        utils.write_config(os.path.abspath("config.ini"), "serial", "port", self.port)

    def on_EditBaudrate(self):
        self.baud_rate = self.baudrateEdit.text()
        utils.write_config(os.path.abspath("config.ini"), "serial", "baudrate", self.baud_rate)

    def on_openCom(self):
        serCom.openCom(self.port, self.baud_rate)

    def on_closeCom(self):
        serCom.closeCom()

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
