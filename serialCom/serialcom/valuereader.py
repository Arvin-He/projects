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

from utils import read_config, write_config, read_txt
from log import logger, fh
import serialcom as serCom
from serialcom_ui import Ui_serialDlg as serialDlg
import serialdb


colors = ['#7fc97f', '#beaed4', '#fdc086', '#ffff99',
          '#386cb0', '#f0027f', '#bf5b17', '#666666']


class MainWindow(QDialog, serialDlg):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint |
                            Qt.WindowCloseButtonHint)
        self.com_open = False
        self.data = None
        self.dataList = []
        self.isNewItem = True
        self.productID = 0
        self.initUI()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.on_readData)

    def initUI(self):
        self.infoLabel.setText("信息:")
        self.port = read_config(
            os.path.abspath("config/config.ini"), "serial", "port")
        self.baud_rate = read_config(
            os.path.abspath("config/config.ini"), "serial", "baudrate")
        self.time_out = read_config(
            os.path.abspath("config/config.ini"), "serial", "timeout")
        self.group_count = read_config(
            os.path.abspath("config/config.ini"), "group", "count")
        self.barcode_path = read_config(
            os.path.abspath("config/config.ini"), "barcode", "barcode_path")

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
        write_config(os.path.abspath("config/config.ini"),
                     "serial", "port", self.port)

    def on_editBaudrate(self):
        self.baud_rate = self.baudrateEdit.text()
        write_config(os.path.abspath("config/config.ini"),
                     "serial", "baudrate", self.baud_rate)

    def on_editGroupCount(self):
        self.group_count = self.groupCountEdit.text()
        write_config(os.path.abspath("config/config.ini"),
                     "group", "count", self.group_count)

    def on_openCom(self):
        self.com_open = serCom.openCom(
            self.port, self.baud_rate, int(self.time_out))
        if self.com_open is True:
            self.infoLabel.setText("信息:串口{}打开成功!".format(self.port))
        else:
            self.infoLabel.setText("信息:串口{}打开失败!".format(self.port))

    def on_closeCom(self):
        if serCom.closeCom():
            self.infoLabel.setText("信息:串口{}关闭!".format(self.port))
        else:
            self.infoLabel.setText("信息:串口{}没有打开,不需要关闭!".format(self.port))

    def on_startRead(self):
        if self.com_open is True:
            self.infoLabel.setText("信息:开始读取串口数据...")
            # 启动定时器
            self.timer.start(50)
        else:
            self.infoLabel.setText("信息:串口{}没有通讯成功!".format(self.port))

    def on_stopRead(self):
        if self.com_open is True:
            # 关掉定时器
            self.timer.stop()
            self.infoLabel.setText("信息:停止串口{}读取数据...".format(self.port))
        else:
            self.infoLabel.setText("信息:串口{}没有通讯成功!".format(self.port))

    # def on_readBarcode(self):
    #     pass
        # if self.isBoth:
        #     pass
        # else:
        #     if not self.barcodeEdit.hasFocus():
        #         self.barcodeEdit.setFocus()
        #     if len(self.barcodeEdit.text()) != 21:
        #         if len(self.barcodeEdit.text()) > 21:
        #             # 截取最后21位字符串
        #             self.barcodeEdit.setText(self.barcodeEdit.text()[-21:])
        #         else:
        #             self.barcodeEdit.setText("")

    # 定时写数据读数据
    def on_readData(self):
        if serCom.writeData():
            time.sleep(0.005)
            self.data = serCom.readData()
            if self.data is not None:
                self.showData()
                self.saveData()
        else:
            logger.info("发送指令失败,定时器关闭...")
            self.timer.stop()

    # 显示数据
    def showData(self):
        # 显示状态位
        self.showState()
        if self.data[2] == 2 or self.data[2] == 3:
            self.recvHexEdit.setText(str(self.data[0]))
            self.transValEdit.setText(str(self.data[1]))
            self.flagBitEdit.setText(str(self.data[2]))
            self.tightTorqueEdit.setText(str(self.data[3]))
            self.tightAngleEdit.setText(str(self.data[4]))
        self.showDataOnPanel()

    # 显示状态位
    def showState(self):
        if self.data[2] == 2:
            self.flagBitLabel.setText("OK")
            self.flagBitLabel.setStyleSheet(
                "QLabel{color: green; background-color: black;}")
        elif self.data[2] == 3:
            self.flagBitLabel.setText("NG")
            self.flagBitLabel.setStyleSheet(
                "QLabel{color: red; background-color: black;}")
        else:
            self.flagBitLabel.setText("")
            self.flagBitLabel.setStyleSheet(
                "QLabel{background-color: transparent;}")

    def showDataOnPanel(self):
        if self.data[2] == 2 or self.data[2] == 3:
            my_data = [self.data[0], self.data[1],
                       self.data[2], self.data[3], self.data[4]]
            # 如果满8个数据,就清空dataList
            if len(self.dataList) == int(self.group_count) * 2:
                self.dataList.clear()
                self.isNewItem = True
            self.dataList.append(my_data)
            # 清空面板
            self.dataListPanel.clear()
            if self.dataListPanel.item(0) is None:
                header = "拧紧力矩".rjust(8) + "拧紧角度".rjust(16) + "状态位".rjust(16)
                self.dataListPanel.addItem(QtWidgets.QListWidgetItem(header))          
            for i, item in enumerate(reversed(self.dataList)):
                flagBit = self.dataList[i][2]
                tightTorque = self.dataList[i][3]
                tightAngle = self.dataList[i][4]
                item_text = "{:>11}".format(tightTorque) + "{:>20}".format(
                    tightAngle) + "{:>22}".format(flagBit)
                item = QtWidgets.QListWidgetItem(item_text)
                if i in range(0, 2):
                    item.setBackground(QtGui.QColor("#7fc97f"))
                elif i in range(2, 4):
                    item.setBackground(QtGui.QColor("#beaed4"))
                elif i in range(4, 6):
                    item.setBackground(QtGui.QColor("#fdc086"))
                elif i in range(6, 8):
                    item.setBackground(QtGui.QColor("#ffff99"))
                self.dataListPanel.addItem(item)
        print("datalist_len = ", len(self.dataList))
        print("datalist = ", self.dataList)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    def on_showPre(self):
        self.productID -= 1
        productInfo = serialdb.query_productInfoByID(self.productID)
        self.showInfo(productInfo)

    def on_showNext(self):
        self.productID += 1
        productInfo = serialdb.query_productInfoByID(self.productID)
        self.showInfo(productInfo)

    def on_showProductInfo(self):
        productInfo = serialdb.query_productInfo()
        self.showInfo(productInfo)

    def showInfo(self, productInfo):
        self.productInfoPanel.clear()
        if productInfo is not None:
            product_id = "产品ID:{}".format(productInfo["id"])
            self.productID = int(productInfo["id"])
            barcode = "条形码:   {}".format(productInfo["barcode"])
            tightTorque = "拧紧力矩:  {}".format(productInfo["tight_torque"])
            tightAngle = "拧紧角度:  {}".format(productInfo["tight_angle"])
            date_time = "日期-时间: {}".format(productInfo["record_date"])
            self.productInfoPanel.addItem(QtWidgets.QListWidgetItem("产品信息明细:"))
            self.productInfoPanel.addItem(
                QtWidgets.QListWidgetItem(product_id))
            self.productInfoPanel.addItem(QtWidgets.QListWidgetItem(barcode))
            self.productInfoPanel.addItem(
                QtWidgets.QListWidgetItem(tightTorque))
            self.productInfoPanel.addItem(
                QtWidgets.QListWidgetItem(tightAngle))
            self.productInfoPanel.addItem(QtWidgets.QListWidgetItem(date_time))
        else:
            self.productInfoPanel.addItem(QtWidgets.QListWidgetItem("产品明细: 无"))
        
    def get_barcode(self):
        read_txt(self.barcode_path)
        # pass
        # barcode = self.barcodeEdit.text()
        # if len(barcode) == 21 or len(barcode) == 18:
        #     return barcode
        # else:
        #     return ""

    def get_flagbit(self):
        flags = []
        for item in self.dataList:
            flags.append(item[2])
        return flags

    def get_tight_torque(self):
        torques = []
        for item in self.dataList:
            torques.append(item[3])
        return torques

    def get_tight_angle(self):
        angles = []
        for item in self.dataList:
            angles.append(item[4])
        return angles

    def saveData(self):
        barcodes = self.get_barcode()
        flags = self.get_flagbit()
        torques = self.get_tight_torque()
        angles = self.get_tight_angle()
        if barcodes or (flags and torques and angles):
            if self.isNewItem:
                serialdb.insert_productItem(barcode=barcodes,
                                            flag_bit=flags,
                                            tight_torque=torques,
                                            tight_angle=angles)
                self.isNewItem = False
            else:
                serialdb.update_productItem(barcode=barcodes,
                                            flag_bit=flags,
                                            tight_torque=torques,
                                            tight_angle=angles)

    def done(self, result):
        super(MainWindow, self).done(result)
        logger.info("close application")
        fh.flush()
        fh.close()
        self.close()
