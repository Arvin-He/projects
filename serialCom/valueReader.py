# usr/bin/python3
# -*- coding:utf-8 -*-
import os
import sys
import time
import copy
from datetime import datetime
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
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
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint |
                            Qt.WindowCloseButtonHint)
        self.data = {}
        self.old_data = {}
        self.initUI()
        self.lastdata = ["", ""]
        self.showdata = []
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.on_readData)
        self.showDatasOnPanel()

    def initUI(self):
        self.infoLabel.setText("信息:")
        self.port = utils.read_config(
            os.path.abspath("config.ini"), "serial", "port")
        self.baud_rate = utils.read_config(
            os.path.abspath("config.ini"), "serial", "baudrate")
        self.group_count = utils.read_config(
            os.path.abspath("config.ini"), "group", "count")

        self.portEdit.setText(self.port)
        self.baudrateEdit.setText(self.baud_rate)
        self.groupCountEdit.setText(self.group_count)

        self.openBtn.clicked.connect(self.on_openCom)
        self.closeBtn.clicked.connect(self.on_closeCom)
        self.startReadBtn.clicked.connect(self.on_startRead)
        self.stopReadBtn.clicked.connect(self.on_stopRead)
        self.portEdit.editingFinished.connect(self.on_editPortName)
        self.baudrateEdit.editingFinished.connect(self.on_editBaudrate)
        self.groupCountEdit.editingFinished.connect(self.on_editGroupCount)
        self.preBtn.clicked.connect(self.on_showPre)
        self.nextBtn.clicked.connect(self.on_showNext)

    def on_editPortName(self):
        self.port = self.portEdit.text()
        utils.write_config(os.path.abspath("config.ini"),
                           "serial", "port", self.port)

    def on_editBaudrate(self):
        self.baud_rate = self.baudrateEdit.text()
        utils.write_config(os.path.abspath("config.ini"),
                           "serial", "baudrate", self.baud_rate)

    def on_editGroupCount(self):
        self.group_count = self.groupCountEdit.text()
        utils.write_config(os.path.abspath("config.ini"),
                           "group", "count", self.group_count)

    def on_showPre(self):
        pass

    def on_showNext(self):
        pass

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
            # 在获取新数据前保存上一次的值
            self.old_data = copy.deepcopy(self.data)
            self.getData()
            self.showData()
            self.showState()
        else:
            logger.info("发送指令失败,定时器关闭...")
            self.timer.stop()

    # 读取串口数据,并提取数据
    def getData(self):
        self.data["recv"] = serCom.readData()
        if recv_data:
            # 转换收到的数据
            self.data["trans"] = serCom.transformData(self.data["recv"])
            self.data["process"] = serCom.processData(self.data["trans"])
            self.data["flagBit"] = serCom.getFlagBit(self.data["process"])
            self.data["tightTorque"] = serCom.getTightTorque(
                self.data["process"])
            self.data["tightAngle"] = serCom.getTightAngle(
                self.data["process"])
        else:
            logger.warn("recev no data")

    # 显示数据
    def showData(self):
        self.recvHexEdit.setText(self.data["recv"])
        self.transValEdit.setText(self.data["trans"])
        self.flagBitEdit.setText(self.data["flagBit"])
        if self.data["flagBit"] == "2" or self.data["flagBit"] == "3":
            self.tightTorqueEdit.setText(self.data["tightTorque"])
            self.tightAngleEdit.setText(self.data["tightAngle"])
            # # 去重
            # if self.lastdata and (self.lastdata[0] != tightTorque or self.lastdata[1] != tightAngle):
            #     if len(self.showdata) < 10:
            #         self.showdata.append(
            #             (flagBit, tightTorque, tightAngle))
            #     else:
            #         self.showdata.remove(self.showdata[0])
            #         self.showdata.append(
            #             (flagBit, tightTorque, tightAngle))
            #     self.showDataOnTable()
            #     csv_data = [flagBit, tightTorque, tightAngle,
            #                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            #     csvData.saveCSV(csv_data)
        else:
            self.tightTorqueEdit.setText("")
            self.tightAngleEdit.setText("")

    # 显示状态
    def showState(self):
        if self.data["flagBit"] == "2":
            self.flagBitLabel.setStyleSheet(
                "QLabel{background-color: green;}")
        elif self.data["flagBit"] == "3":
            self.flagBitLabel.setStyleSheet(
                "QLabel{background-color: red;}")
        else:
            self.flagBitLabel.setStyleSheet(
                "QLabel{background-color: transparent;}")

    def showDatasOnPanel(self):
        format_text = self.formatText()
        text = "\n".join(format_text)
        self.dataPanel.setText(text)

    def formatText(self):
        text_list = []
        header = "拧紧力矩".rjust(20)+"拧紧角度".rjust(20)
        text_list.append(header)
        for i in range(int(self.group_count)):
            text_list.append("{}号螺丝: ".format(i+1))
        return text_list

    def showDataOnTable(self):
        data_num = len(self.showdata)
        for i in range(data_num):
            pass
            # new_item0 = QTableWidgetItem(self.showdata[data_num-1-i][0])
            # new_item1 = QTableWidgetItem(self.showdata[data_num-1-i][1])
            # new_item2 = QTableWidgetItem(self.showdata[data_num-1-i][2])
            # self.dataTable.setItem(i, 0, new_item0)
            # self.dataTable.setItem(i, 1, new_item1)
            # self.dataTable.setItem(i, 2, new_item2)

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
