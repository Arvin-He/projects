# usr/bin/python3
# -*- coding:utf-8 -*-
import os
import sys
import time
import copy
from datetime import datetime
from PyQt5 import QtGui
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

import utils
from logger import logger, fh
import serialComm as serCom
from serialCom_ui import Ui_serialDlg as serialDlg
import serialdb


app = QtWidgets.QApplication(sys.argv)
colors = ['#7fc97f', '#beaed4', '#fdc086', '#ffff99',
          '#386cb0', '#f0027f', '#bf5b17', '#666666']


class MainWindow(QDialog, serialDlg):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint |
                            Qt.WindowCloseButtonHint)
        self.data = {}
        self.old_data = {}
        self.tightTorqueList = []
        self.tightAngleList = []
        self.productID = 0
        self.initUI()
        self.barcodeEdit.setFocus()
        self.timer = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()
        self.timer.timeout.connect(self.on_readData)
        self.timer2.timeout.connect(self.on_setFocusInBarcodeEdit)
        # self.showProductInfo()
        self.timer2.start(3000)
        # self.showDataOnPanel()
        # self.saveData()

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
        self.currBtn.clicked.connect(self.on_showProductInfo)
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

    def on_setFocusInBarcodeEdit(self):
        if not self.barcodeEdit.hasFocus():
            self.barcodeEdit.setFocus()

    # 定时写数据读数据
    def on_readData(self):
        if serCom.writeData():
            time.sleep(0.005)
            # 在获取新数据前保存上一次的值
            self.old_data = copy.deepcopy(self.data)
            self.getData()
            # 去重
            self.dedupData()
            self.showData()
            self.saveData()
        else:
            logger.info("发送指令失败,定时器关闭...")
            self.timer.stop()

    # 读取串口数据,并提取数据
    def getData(self):
        self.data["recev"] = serCom.readData()
        if self.data["recev"]:
            # 转换收到的数据
            self.data["trans"] = serCom.transformData(self.data["recev"])
            self.data["process"] = serCom.processData(self.data["trans"])
            self.data["flagBit"] = serCom.getFlagBit(self.data["process"])
            self.data["tightTorque"] = serCom.getTightTorque(
                self.data["process"])
            self.data["tightAngle"] = serCom.getTightAngle(
                self.data["process"])
        else:
            logger.warn("recev no data")

    # 去除重复数据
    def dedupData(self):
        if self.old_data["tightTorque"] != self.data["tightTorque"] or self.old_data["tightAngle"] != self.data[
                "tightAngle"]:
            if len(self.tightTorqueList) >= self.group_count * 2:
                del self.tightTorqueList[0]
                del self.tightAngleList[0]
            self.tightTorqueList.append(self.data["tightTorque"])
            self.tightAngleList.append(self.data["tightAngle"])

    # 显示数据
    def showData(self):
        self.recvHexEdit.setText(self.data["recev"])
        self.transValEdit.setText(self.data["trans"])
        self.flagBitEdit.setText(self.data["flagBit"])
        # 显示状态位
        self.showState()
        if self.data["flagBit"] == "2" or self.data["flagBit"] == "3":
            self.tightTorqueEdit.setText(self.data["tightTorque"])
            self.tightAngleEdit.setText(self.data["tightAngle"])
        else:
            self.tightTorqueEdit.setText("")
            self.tightAngleEdit.setText("")
        self.showDataOnPanel()

    # 显示状态位
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

    def showDataOnPanel(self):
        header = "拧紧力矩".rjust(16) + "拧紧角度".rjust(16)
        self.dataListPanel.addItem(QtWidgets.QListWidgetItem(header))
        count = len(self.tightTorqueList)
        for i in range(count):
            tightTorque = self.tightTorqueList[count - i - 1]
            tightAngle = self.tightAngleList[count - i - 1]
            item_text = "{:>16}".format(tightTorque) + "{:>25}".format(tightAngle)
            item = QtWidgets.QListWidgetItem(item_text)
            if i == 0:
                item.setBackground(QtGui.QColor("#7fc97f"))
            self.dataListPanel.addItem(item)

    def on_showPre(self):
        if self.productID is not None:
            ID = self.productID -1
            if ID > 0 :
                productInfo = serialdb.query_productInfoByID(ID)
                self.showInfo(productInfo)

    def on_showNext(self):
        if self.productID is not None:
            ID = self.productID + 1
            if ID > 0 :
                productInfo = serialdb.query_productInfoByID(ID)
                self.showInfo(productInfo)

    def on_showProductInfo(self):
        productInfo = serialdb.query_productInfo()
        self.showInfo(productInfo)

    def showInfo(self, info):
        productInfo = info
        header = "产品信息明细:"
        self.productInfoPanel.addItem(QtWidgets.QListWidgetItem(header))
        product_id = "产品ID:{}".format(productInfo["id"])
        self.productID = int(productInfo["id"]) if productInfo["id"] else None
        self.productInfoPanel.addItem(QtWidgets.QListWidgetItem(product_id))
        barcode = "条形码:   {}".format(productInfo["barcode"])
        self.productInfoPanel.addItem(QtWidgets.QListWidgetItem(barcode))
        tightTorque = "拧紧力矩:  {}".format(productInfo["tight_torque"])
        self.productInfoPanel.addItem(QtWidgets.QListWidgetItem(tightTorque))
        tightAngle = "拧紧角度:  {}".format(productInfo["tight_angle"])
        self.productInfoPanel.addItem(QtWidgets.QListWidgetItem(tightAngle))
        date_time = "日期-时间: {}".format(productInfo["record_date"])
        self.productInfoPanel.addItem(QtWidgets.QListWidgetItem(date_time))

    def get_barcode(self):
        return self.barcodeEdit.text()

    def get_tight_torque(self):
        tight_torque_dict = {}
        tight_torque_dict["tight_torque"] = self.tightTorqueList
        return tight_torque_dict

    def get_tight_angle(self):
        tight_angle_dict = {}
        tight_angle_dict["tight_angle"] = self.tightAngleList
        return tight_angle_dict

    def saveData(self):
        if len(self.tightTorqueList) == self.group_count * 2:
            serialdb.insert_productItem(barcode=self.get_barcode(),
                                        tight_torque=self.get_tight_torque(),
                                        tight_angle=self.get_tight_angle())

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
