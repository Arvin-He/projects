# -*- coding:utf-8 -*-
import os
import time
from PyQt5 import QtGui
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from utils import read_config, write_config
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
        # self.data = None
        # self.dataList = []
        self.isNewItem = True
        self.lastdata = ["", ""]
        self.productID = 0
        self.lastdata = ["", ""]
        self.showdata = []
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
            self.timer.start(200)
        else:
            self.infoLabel.setText("信息:串口{}没有通讯成功!".format(self.port))

    def on_stopRead(self):
        if self.com_open is True:
            # 关掉定时器
            self.timer.stop()
            self.infoLabel.setText("信息:停止串口{}读取数据...".format(self.port))
        else:
            self.infoLabel.setText("信息:串口{}没有通讯成功!".format(self.port))

    def updateFlag(self, flagBit):
        if flagBit == "2":
            self.flagBitLabel.setStyleSheet(
                "QLabel{background-color: green;}")
        elif flagBit == "3":
            self.flagBitLabel.setStyleSheet(
                "QLabel{background-color: red;}")
        else:
            self.flagBitLabel.setStyleSheet(
                "QLabel{background-color: transparent;}")

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
                self.flagBitEdit.setText(flagBit)
                self.updateFlag(flagBit)

                tightTorque = serCom.getTightTorque(process_data)
                tightAngle = serCom.getTightAngle(process_data)
                if flagBit == "2" or flagBit == "3":
                    self.tightTorqueEdit.setText(tightTorque)
                    self.tightAngleEdit.setText(tightAngle)

                    if self.lastdata and (self.lastdata[0] != tightTorque or self.lastdata[1] != tightAngle):
                        if len(self.showdata) < 8:
                            self.showdata.append([flagBit, tightTorque, tightAngle])
                        else:
                            # self.showdata.remove(self.showdata[0])
                            self.showdata.clear()
                            self.showdata.append([flagBit, tightTorque, tightAngle])
                        self.showData()
                else:
                    self.tightTorqueEdit.setText("")
                    self.tightAngleEdit.setText("")
                # 保存上一次的值
                self.lastdata[0] = tightTorque
                self.lastdata[1] = tightAngle
            else:
                logger.info("recev no data")
        else:
            logger.info("发送指令失败,定时器关闭...")
            self.timer.stop()

    # 显示数据
    def showData(self):
        # 清空面板
        self.dataListPanel.clear()
        if self.dataListPanel.item(0) is None:
            header = "拧紧力矩".rjust(8) + "拧紧角度".rjust(16) + "状态位".rjust(16)
            self.dataListPanel.addItem(QtWidgets.QListWidgetItem(header))          
        for i, item in enumerate(reversed(self.showdata)):
            if i in range(0, 2):
                item.setBackground(QtGui.QColor("#7fc97f"))
            elif i in range(2, 4):
                item.setBackground(QtGui.QColor("#beaed4"))
            elif i in range(4, 6):
                item.setBackground(QtGui.QColor("#fdc086"))
            elif i in range(6, 8):
                item.setBackground(QtGui.QColor("#ffff99"))
            flagBit, tightTorque, tightAngle = item[0], item[1], item[2]
            item_text = "{:>11}".format(tightTorque) + "{:>20}".format(
                tightAngle) + "{:>22}".format(flagBit)
            list_item = QtWidgets.QListWidgetItem(item_text)
            self.dataListPanel.addItem(list_item)


    # # 定时写数据读数据
    # def on_readData(self):
    #     if serCom.writeData():
    #         time.sleep(0.005)
    #         self.data = serCom.readData()
    #         logger.info("self.data = {}".format(self.data))
    #         try:
    #             if self.data:
    #                 self.showData()
    #                 self.saveData()
    #         except Exception as e:
    #             logger.error(e)
    #             return
    #     else:
    #         logger.info("发送指令失败,定时器关闭...")
    #         self.timer.stop()

    # 显示数据
    # def showData(self):
    #     # 显示状态位
    #     self.showState()
    #     if self.data[2] == 2 or self.data[2] == 3:
    #         self.recvHexEdit.setText(str(self.data[0]))
    #         self.transValEdit.setText(str(self.data[1]))
    #         self.flagBitEdit.setText(str(self.data[2]))
    #         self.tightTorqueEdit.setText(str(self.data[3]))
    #         self.tightAngleEdit.setText(str(self.data[4]))
    #     self.showDataOnPanel()

    # 显示状态位
    # def showState(self):
    #     if self.data[2] == 2:
    #         self.flagBitLabel.setText("OK")
    #         self.flagBitLabel.setStyleSheet(
    #             "QLabel{color: green; background-color: black;}")
    #     elif self.data[2] == 3:
    #         self.flagBitLabel.setText("NG")
    #         self.flagBitLabel.setStyleSheet(
    #             "QLabel{color: red; background-color: black;}")
    #     else:
    #         self.flagBitLabel.setText("")
    #         self.flagBitLabel.setStyleSheet(
    #             "QLabel{background-color: transparent;}")

    # def showDataOnPanel(self):
    #     if self.data[2] == 2 or self.data[2] == 3:
    #         my_data = [self.data[0], self.data[1],
    #                    self.data[2], self.data[3], self.data[4]]
    #         # 如果满8个数据,就清空dataList
    #         if len(self.dataList) == int(self.group_count) * 2:
    #             self.dataList.clear()
    #             self.isNewItem = True
    #         self.dataList.append(my_data)
    #         # 清空面板
    #         self.dataListPanel.clear()
    #         if self.dataListPanel.item(0) is None:
    #             header = "拧紧力矩".rjust(8) + "拧紧角度".rjust(16) + "状态位".rjust(16)
    #             self.dataListPanel.addItem(QtWidgets.QListWidgetItem(header))          
    #         for i, item in enumerate(reversed(self.dataList)):
    #             flagBit = self.dataList[i][2]
    #             tightTorque = self.dataList[i][3]
    #             tightAngle = self.dataList[i][4]
    #             item_text = "{:>11}".format(tightTorque) + "{:>20}".format(
    #                 tightAngle) + "{:>22}".format(flagBit)
    #             item = QtWidgets.QListWidgetItem(item_text)
    #             if i in range(0, 2):
    #                 item.setBackground(QtGui.QColor("#7fc97f"))
    #             elif i in range(2, 4):
    #                 item.setBackground(QtGui.QColor("#beaed4"))
    #             elif i in range(4, 6):
    #                 item.setBackground(QtGui.QColor("#fdc086"))
    #             elif i in range(6, 8):
    #                 item.setBackground(QtGui.QColor("#ffff99"))
    #             self.dataListPanel.addItem(item)

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

    def show_barcode(self):
        self.check_barcodefiles(self.barcode_path)
        for txt in os.listdir(self.barcode_path):
            barcode_info = os.path.splitext(txt)[0].split('_')
            barcode_name = barcode_info[0]
            barcode = barcode_info[1]
            if barcode_name == "barCode1":
                self.barcodeEdit.setText(barcode)
            if barcode_name == "barCode2":
                self.barcodeEdit_2.setText(barcode)

    def get_barcode(self):
        self.show_barcode()
        barcode = ''
        barcode1 = self.barcodeEdit.text()
        barcode2 = self.barcodeEdit_2.text()
        if barcode1 and barcode2:
            self.delete_file('barCode1')
            return barcode1
        elif barcode1 and not barcode2:
            return barcode1
        elif barcode2 and not barcode1:
            return barcode2
        else:
            return barcode

    def delete_file(self, file_name):
        for txt in os.listdir(self.barcode_path):
            if txt.startswith(file_name):
                os.remove(os.path.join(self.barcode_path, txt))

    def check_barcodefiles(self, barcodes_path):
        file_list = os.listdir(barcodes_path)
        # 将文件按照修改时间排序, 最新修改的排在最前面
        file_list.sort(key=lambda fn: os.path.getmtime(os.path.join(barcodes_path, fn))
            if not os.path.isdir(os.path.join(barcodes_path, fn)) else 0)
        if len(file_list) > 2:
            for i, txt_file in enumerate(file_list):
                if i > 1:
                    os.remove(os.path.join(barcodes_path, txt_file))

    def get_flagbit(self):
        flags = []
        for item in self.showdata():
            flags.append(item[0])
        # for item in self.dataList:
        #     flags.append(item[2])
        return flags

    def get_tight_torque(self):
        torques = []
        for item in self.showdata():
            torques.append(item[1])
        # for item in self.dataList:
        #     torques.append(item[3])
        return torques

    def get_tight_angle(self):
        angles = []
        for item in self.showdata():
            angles.append(item[2])
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
