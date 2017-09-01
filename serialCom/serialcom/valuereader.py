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
        self.data = {"recev": None, "trans": None, "process": None,
                     "flagBit": None, "tightTorque": None, "tightAngle": None}
        self.old_data = {"recev": None, "trans": None, "process": None,
                         "flagBit": None, "tightTorque": None, "tightAngle": None}
        self.tightTorqueList = []
        self.tightAngleList = []
        self.flagBitList = []
        self.isNewItem = True
        self.productID = 0
        self.initUI()
        self.barcodeEdit.setFocus()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.on_readData)

        self.timer2 = QtCore.QTimer()
        self.timer2.timeout.connect(self.on_readBarcode)
        self.timer2.start(3000)
        # self.t1 = threading.Thread(target=self.start_read_barcode)
        # self.t1.start()
        # self.timer2.timeout.connect(self.on_setFocusInBarcodeEdit)
        # self.timer2.start(5000)

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
        self.leftRadioBtn.clicked.connect(self.on_setLeft)
        self.rightRadioBtn.clicked.connect(self.on_setRight)
        self.bothRadioBtn.clicked.connect(self.on_setBoth)

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

    def on_readBarcode(self):
        if not self.barcodeEdit.hasFocus():
            self.barcodeEdit.setFocus()
        if len(self.barcodeEdit.text()) != 21:
            if len(self.barcodeEdit.text()) > 21:
                # 截取最后21位字符串
                self.barcodeEdit.setText(self.barcodeEdit.text()[-21:])
            else:
                self.barcodeEdit.setText("")

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
        count = len(self.tightTorqueList)
        # 4个螺丝一组,显示8个值,满8个数值就清空
        if count == int(self.group_count) * 2:
            self.isNewItem = True
            self.tightTorqueList.clear()
            self.tightAngleList.clear()
            self.flagBitList.clear()
        else:
            self.isNewItem = False
        # 去重,每50ms读取一次值,取用新值,删除旧值
        if self.data["flagBit"] == "2" or self.data["flagBit"] == "3":
            if self.old_data["tightTorque"] is None and self.old_data["tightAngle"] is None:
                self.tightTorqueList.append(self.data["tightTorque"])
                self.tightAngleList.append(self.data["tightAngle"])
                self.flagBitList.append(self.data["flagBit"])
            else:
                if not (self.old_data["tightTorque"] == self.data["tightTorque"] and
                        self.old_data["tightAngle"] == self.data["tightAngle"]):
                    self.tightTorqueList.append(self.data["tightTorque"])
                    self.tightAngleList.append(self.data["tightAngle"])
                    self.flagBitList.append(self.data["flagBit"])

            # self.tightTorqueList.append(self.data["tightTorque"])
            # self.tightAngleList.append(self.data["tightAngle"])
            # self.flagBitList.append(self.data["flagBit"])
            # if self.old_data and self.old_data["tightTorque"] == self.data["tightTorque"] and \
            #         self.old_data["tightAngle"] == self.data["tightAngle"]:
            #     del self.tightTorqueList[count - 1]
            #     del self.tightAngleList[count - 1]
            #     del self.flagBitList[count - 1]

    # 显示数据
    def showData(self):
        self.recvHexEdit.setText(self.data["recev"])
        self.transValEdit.setText(self.data["process"])
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
            self.flagBitLabel.setText("OK")
            self.flagBitLabel.setStyleSheet(
                "QLabel{color: green; background-color: black;}")
        elif self.data["flagBit"] == "3":
            self.flagBitLabel.setText("NG")
            self.flagBitLabel.setStyleSheet(
                "QLabel{color: red; background-color: black;}")
        else:
            self.flagBitLabel.setText("")
            self.flagBitLabel.setStyleSheet(
                "QLabel{background-color: transparent;}")

    def showDataOnPanel(self):
        self.dataListPanel.clear()
        if self.dataListPanel.item(0) is None:
            header = "拧紧力矩".rjust(8) + "拧紧角度".rjust(16) + "状态位".rjust(16)
            self.dataListPanel.addItem(QtWidgets.QListWidgetItem(header))
        count = len(self.tightTorqueList)
        for i in range(count):
            tightTorque = self.tightTorqueList[count - i - 1]
            tightAngle = self.tightAngleList[count - i - 1]
            flagBit = self.flagBitList[count - i - 1]
            item_text = "{:>11}".format(
                tightTorque) + "{:>20}".format(tightAngle) + "{:>22}".format(flagBit)
            item = QtWidgets.QListWidgetItem(item_text)
            if i == 0:
                item.setBackground(QtGui.QColor("#7fc97f"))
            self.dataListPanel.addItem(item)

    def on_showPre(self):
        self.productID -= 1
        logger.info("pre_id = {}".format(self.productID))
        productInfo = serialdb.query_productInfoByID(self.productID)
        self.showInfo(productInfo)

    def on_showNext(self):
        self.productID += 1
        logger.info("next_id = {}".format(self.productID))
        productInfo = serialdb.query_productInfoByID(self.productID)
        self.showInfo(productInfo)

    def on_showProductInfo(self):
        productInfo = serialdb.query_productInfo()
        logger.info(productInfo)
        self.showInfo(productInfo)

    def showInfo(self, productInfo):
        self.productInfoPanel.clear()
        header = "产品信息明细:"
        product_id = "产品ID:"
        barcode = "条形码:"
        tightTorque = "拧紧力矩:"
        tightAngle = "拧紧角度:"
        date_time = "日期-时间:"
        if productInfo is not None:
            product_id = "产品ID:{}".format(productInfo["id"])
            self.productID = int(productInfo["id"])
            barcode = "条形码:   {}".format(productInfo["barcode"])
            tightTorque = "拧紧力矩:  {}".format(productInfo["tight_torque"])
            tightAngle = "拧紧角度:  {}".format(productInfo["tight_angle"])
            date_time = "日期-时间: {}".format(productInfo["record_date"])
            self.productInfoPanel.addItem(QtWidgets.QListWidgetItem(header))
            # logger.info("productID = {}".format(self.productID))
            self.productInfoPanel.addItem(QtWidgets.QListWidgetItem(product_id))
            self.productInfoPanel.addItem(QtWidgets.QListWidgetItem(barcode))
            self.productInfoPanel.addItem(QtWidgets.QListWidgetItem(tightTorque))
            self.productInfoPanel.addItem(QtWidgets.QListWidgetItem(tightAngle))
            self.productInfoPanel.addItem(QtWidgets.QListWidgetItem(date_time))
        else:
            self.productInfoPanel.addItem(QtWidgets.QListWidgetItem("产品明细: 无"))


    def get_barcode(self):
        barcode = self.barcodeEdit.text()
        if len(barcode) == 21:
            return barcode
        else:
            return ""

    def get_tight_torque(self):
        tight_torque_dict = {}
        tight_torque_dict["tight_torque"] = self.tightTorqueList
        return tight_torque_dict

    def get_tight_angle(self):
        tight_angle_dict = {}
        tight_angle_dict["tight_angle"] = self.tightAngleList
        return tight_angle_dict

    def saveData(self):
        if self.isNewItem:
            serialdb.insert_productItem(barcode=self.get_barcode(),
                                        tight_torque=self.get_tight_torque(),
                                        tight_angle=self.get_tight_angle())
        else:
            serialdb.update_productItem(barcode=self.get_barcode(),
                                        tight_torque=self.get_tight_torque(),
                                        tight_angle=self.get_tight_angle())

    def on_setLeft(self):
        self.leftRadioBtn.setChecked(True)
        self.barcodeEdit.setEnabled(True)
        self.barcodeEdit_2.setEnabled(False)
        self.barcodeEdit.setFocus()

    def on_setRight(self):
        self.rightRadioBtn.setChecked(True)
        self.barcodeEdit.setEnabled(False)
        self.barcodeEdit_2.setEnabled(True)
        self.barcodeEdit_2.setFocus()

    def on_setBoth(self):
        self.bothRadioBtn.setChecked(True)
        self.barcodeEdit.setEnabled(True)
        self.barcodeEdit_2.setEnabled(True)
        self.barcodeEdit.setFocus()

    def done(self, result):
        super(MainWindow, self).done(result)
        logger.info("close application")
        fh.flush()
        fh.close()
        self.close()
