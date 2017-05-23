# usr/bin/python3
# -*- coding:utf-8 -*-
import os
import sys
import time
from datetime import datetime
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView

import utils
import csvData
from logger import logger, fh
import serialComm as serCom
from serialCom_ui import Ui_serialDlg as serialDlg

app = QtWidgets.QApplication(sys.argv)


class MainWindow(QDialog, serialDlg):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.initUI()
        self.lastdata = ["", ""]
        self.showdata = []
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.on_readData)

    def initUI(self):
        self.dataTable.setColumnWidth(0, 50)
        self.dataTable.setColumnWidth(1, 70)
        self.dataTable.setColumnWidth(2, 70)
        self.dataTable.setRowCount(10)
        self.dataTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.dataTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.dataTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
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
        if serCom.openCom(self.port, self.baud_rate):
            self.infoLabel.setText("信息:串口{}打开成功!".format(self.port))
        else:
            self.infoLabel.setText("信息:串口{}打开失败!".format(self.port))

    def on_closeCom(self):
        if serCom.closeCom():
            self.infoLabel.setText("信息:串口关闭!")
        else:
            self.infoLabel.setText("信息:串口没有打开,不需要关闭!")

    def on_startRead(self):
        # 启动定时器
        self.timer.start(50)

    # 定时写数据读数据
    def on_readData(self):
        if serCom.writeData():
            time.sleep(0.005)
            recv_data = serCom.readData()
            if recv_data:
                self.recvHexEdit.setText(recv_data)
                # 转换收到的数据
                trans_data = serCom.transformData(recv_data)
                self.transValEdit.setText(trans_data)
                process_data = serCom.processData(trans_data)
                flagBit = serCom.getFlagBit(process_data)
                tightTorque = serCom.getTightTorque(process_data)
                tightAngle = serCom.getTightAngle(process_data)
                self.flagBitEdit.setText(flagBit)
                if flagBit == "2":
                    self.flagBitLabel.setStyleSheet(
                        "QLabel{background-color: green;}")
                elif flagBit == "3":
                    self.flagBitLabel.setStyleSheet(
                        "QLabel{background-color: red;}")
                else:
                    self.flagBitLabel.setStyleSheet(
                        "QLabel{background-color: transparent;}")
                if flagBit == "2" or flagBit == "3":
                    self.tightTorqueEdit.setText(tightTorque)
                    self.tightAngleEdit.setText(tightAngle)

                    if self.lastdata and (self.lastdata[0] != tightTorque or self.lastdata[1] != tightAngle):
                        if len(self.showdata) < 10:
                            self.showdata.append((flagBit, tightTorque, tightAngle))
                        else:
                            self.showdata.remove(self.showdata[0])
                            self.showdata.append((flagBit, tightTorque, tightAngle))
                        self.showDataOnTable()
                        csv_data = [flagBit, tightTorque, tightAngle,
                                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                        csvData.saveCSV(csv_data)
                else:
                    self.tightTorqueEdit.setText("")
                    self.tightAngleEdit.setText("")
                # 保存上一次的值
                self.lastdata[0] = tightTorque
                self.lastdata[1] = tightAngle
            else:
                logger.warn("recev no data")
        else:
            logger.info("发送指令失败,定时器关闭...")
            self.timer.stop()

    def showDataOnTable(self):
        for i in range(len(self.showdata)):
            new_item0 = QTableWidgetItem(self.showdata[i][0])
            new_item1 = QTableWidgetItem(self.showdata[i][1])
            new_item2 = QTableWidgetItem(self.showdata[i][2])
            self.dataTable.setItem(i, 0, new_item0)
            self.dataTable.setItem(i, 1, new_item1)
            self.dataTable.setItem(i, 2, new_item2)

    def on_stopRead(self):
        self.infoLabel.setText("信息:停止串口读取数据!")
        # 关掉定时器
        self.timer.stop()

    def done(self, result):
        super(MainWindow, self).done(result)
        logger.info("close application")
        fh.flush()
        fh.close()
        self.close()
        app.closeAllWindows()


if __name__ == "__main__":
    mainWin = MainWindow()
    mainWinRect = mainWin.geometry()
    mainWin.setFixedSize(mainWinRect.size())
    mainWin.exec_()
