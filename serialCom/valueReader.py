# usr/bin/python3
# -*- coding:utf-8 -*-

import os
import sys
import time
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog

from serialCom_ui import Ui_serialDlg as serialDlg
import utils
import serialComm as serCom

app = QtWidgets.QApplication(sys.argv)


class MainWindow(QDialog, serialDlg):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.initUI()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.on_readData)

    def initUI(self):
        self.infoLabel.setText("信息:")
        self.port = utils.read_config(
            os.path.abspath("config.ini"), "serial", "port")
        self.baud_rate = utils.read_config(
            os.path.abspath("config.ini"), "serial", "baudrate")
        self.portEdit.setText(self.port)
        self.baudrateEdit.setText(self.baud_rate)
        self.openBtn.clicked.connect(self.on_openCom)
        self.closeBtn.clicked.connect(self.on_closeCom)
        self.startReadBtn.clicked.connect(self.on_startRead)
        self.stopReadBtn.clicked.connect(self.on_stopRead)
        self.portEdit.editingFinished.connect(self.on_EditPortName)
        self.baudrateEdit.editingFinished.connect(self.on_EditBaudrate)

    def on_EditPortName(self):
        self.port = self.portEdit.text()
        utils.write_config(os.path.abspath("config.ini"),
                           "serial", "port", self.port)

    def on_EditBaudrate(self):
        self.baud_rate = self.baudrateEdit.text()
        utils.write_config(os.path.abspath("config.ini"),
                           "serial", "baudrate", self.baud_rate)

    def on_openCom(self):
        serCom.openCom(self.port, self.baud_rate)

    def on_closeCom(self):
        serCom.closeCom()

    def on_startRead(self):
        # 启动定时器
        self.timer.start(50)

    # 定时写数据读数据
    def on_readData(self):
        serCom.writeData()
        time.sleep(0.005)
        recv_data = serCom.readData()
        self.recvHexEdit.setText(recv_data)
        # 转换收到的数据
        trans_data = serCom.transformData(recv_data)
        self.transValEdit.setText(trans_data)

        process_data = serCom.processData(trans_data)
        tightTorque = serCom.getTightTorque(process_data)
        self.tightTorqueEdit.setText(tightTorque)
        tightAngle = serCom.getTightAngle(process_data)
        self.tightAngleEdit.setText(tightAngle)

        flagBit = serCom.getFlagBit(process_data)
        if flagBit == "2" or flagBit == "3":
            csv_data = [flagBit, tightTorque, tightAngle]
            serCom.saveCSV(csv_data)

    def on_stopRead(self):
        # 关掉定时器
        self.timer.stop()


if __name__ == "__main__":
    mainWin = MainWindow()
    mainWinRect = mainWin.geometry()
    mainWin.setFixedSize(mainWinRect.size())
    mainWin.exec_()
