# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'boltdetect.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_boltDetectDlg(object):
    def setupUi(self, boltDetectDlg):
        boltDetectDlg.setObjectName("boltDetectDlg")
        boltDetectDlg.resize(1024, 768)
        self.imageViewLabel = QtWidgets.QLabel(boltDetectDlg)
        self.imageViewLabel.setGeometry(QtCore.QRect(10, 10, 500, 500))
        self.imageViewLabel.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.imageViewLabel.setText("")
        self.imageViewLabel.setObjectName("imageViewLabel")
        self.paramSettingBtn = QtWidgets.QPushButton(boltDetectDlg)
        self.paramSettingBtn.setGeometry(QtCore.QRect(830, 240, 170, 50))
        self.paramSettingBtn.setObjectName("paramSettingBtn")
        self.StartBtn = QtWidgets.QPushButton(boltDetectDlg)
        self.StartBtn.setGeometry(QtCore.QRect(830, 320, 170, 50))
        self.StartBtn.setObjectName("StartBtn")
        self.stopBtn = QtWidgets.QPushButton(boltDetectDlg)
        self.stopBtn.setGeometry(QtCore.QRect(830, 410, 170, 50))
        self.stopBtn.setObjectName("stopBtn")
        self.label = QtWidgets.QLabel(boltDetectDlg)
        self.label.setGeometry(QtCore.QRect(530, 40, 80, 30))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(boltDetectDlg)
        self.label_2.setGeometry(QtCore.QRect(530, 110, 80, 30))
        self.label_2.setObjectName("label_2")
        self.groupBox = QtWidgets.QGroupBox(boltDetectDlg)
        self.groupBox.setGeometry(QtCore.QRect(530, 200, 271, 311))
        self.groupBox.setObjectName("groupBox")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 40, 120, 30))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 100, 120, 30))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(20, 170, 120, 30))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(20, 240, 120, 30))
        self.label_6.setObjectName("label_6")
        self.sumEdit = QtWidgets.QLineEdit(self.groupBox)
        self.sumEdit.setGeometry(QtCore.QRect(130, 40, 120, 30))
        self.sumEdit.setObjectName("sumEdit")
        self.goodNumEdit = QtWidgets.QLineEdit(self.groupBox)
        self.goodNumEdit.setGeometry(QtCore.QRect(130, 100, 120, 30))
        self.goodNumEdit.setObjectName("goodNumEdit")
        self.badNumEdit = QtWidgets.QLineEdit(self.groupBox)
        self.badNumEdit.setGeometry(QtCore.QRect(130, 170, 120, 30))
        self.badNumEdit.setObjectName("badNumEdit")
        self.goodPercentEdit = QtWidgets.QLineEdit(self.groupBox)
        self.goodPercentEdit.setGeometry(QtCore.QRect(130, 240, 120, 30))
        self.goodPercentEdit.setObjectName("goodPercentEdit")
        self.statusLabel = QtWidgets.QLabel(boltDetectDlg)
        self.statusLabel.setGeometry(QtCore.QRect(0, 730, 1024, 38))
        self.statusLabel.setStyleSheet("background-color: rgb(0, 0, 255);")
        self.statusLabel.setText("")
        self.statusLabel.setObjectName("statusLabel")
        self.productIDLabel = QtWidgets.QLabel(boltDetectDlg)
        self.productIDLabel.setGeometry(QtCore.QRect(600, 40, 400, 30))
        self.productIDLabel.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.productIDLabel.setText("")
        self.productIDLabel.setObjectName("productIDLabel")
        self.orderIDLabel = QtWidgets.QLabel(boltDetectDlg)
        self.orderIDLabel.setGeometry(QtCore.QRect(600, 110, 400, 30))
        self.orderIDLabel.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.orderIDLabel.setText("")
        self.orderIDLabel.setObjectName("orderIDLabel")
        self.sampleViewLabel = QtWidgets.QLabel(boltDetectDlg)
        self.sampleViewLabel.setGeometry(QtCore.QRect(10, 520, 200, 200))
        self.sampleViewLabel.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.sampleViewLabel.setText("")
        self.sampleViewLabel.setObjectName("sampleViewLabel")
        self.groupBox_2 = QtWidgets.QGroupBox(boltDetectDlg)
        self.groupBox_2.setGeometry(QtCore.QRect(220, 520, 311, 201))
        self.groupBox_2.setObjectName("groupBox_2")
        self.badSerialLabel = QtWidgets.QLabel(self.groupBox_2)
        self.badSerialLabel.setGeometry(QtCore.QRect(10, 30, 50, 30))
        self.badSerialLabel.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.badSerialLabel.setText("")
        self.badSerialLabel.setObjectName("badSerialLabel")
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(70, 30, 100, 30))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.groupBox_2)
        self.label_13.setGeometry(QtCore.QRect(70, 80, 100, 30))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.groupBox_2)
        self.label_14.setGeometry(QtCore.QRect(70, 120, 110, 30))
        self.label_14.setObjectName("label_14")
        self.packMatineStatusLabel = QtWidgets.QLabel(self.groupBox_2)
        self.packMatineStatusLabel.setGeometry(QtCore.QRect(10, 120, 50, 30))
        self.packMatineStatusLabel.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.packMatineStatusLabel.setText("")
        self.packMatineStatusLabel.setObjectName("packMatineStatusLabel")
        self.label_16 = QtWidgets.QLabel(self.groupBox_2)
        self.label_16.setGeometry(QtCore.QRect(70, 160, 100, 30))
        self.label_16.setObjectName("label_16")
        self.badSeriesEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.badSeriesEdit.setGeometry(QtCore.QRect(170, 30, 120, 30))
        self.badSeriesEdit.setObjectName("badSeriesEdit")
        self.blowTimeEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.blowTimeEdit.setGeometry(QtCore.QRect(170, 80, 120, 30))
        self.blowTimeEdit.setObjectName("blowTimeEdit")
        self.packNumEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.packNumEdit.setGeometry(QtCore.QRect(170, 160, 120, 30))
        self.packNumEdit.setObjectName("packNumEdit")

        self.retranslateUi(boltDetectDlg)
        QtCore.QMetaObject.connectSlotsByName(boltDetectDlg)

    def retranslateUi(self, boltDetectDlg):
        _translate = QtCore.QCoreApplication.translate
        boltDetectDlg.setWindowTitle(_translate("boltDetectDlg", "螺栓检测"))
        self.paramSettingBtn.setText(_translate("boltDetectDlg", "参数设定"))
        self.StartBtn.setText(_translate("boltDetectDlg", "开始检测"))
        self.stopBtn.setText(_translate("boltDetectDlg", "停止检测"))
        self.label.setText(_translate("boltDetectDlg", "产品编号:"))
        self.label_2.setText(_translate("boltDetectDlg", "订单编号:"))
        self.groupBox.setTitle(_translate("boltDetectDlg", "检测结果"))
        self.label_3.setText(_translate("boltDetectDlg", "检测总数目(个):"))
        self.label_4.setText(_translate("boltDetectDlg", "检测合格数目(个):"))
        self.label_5.setText(_translate("boltDetectDlg", "检测排除数目(个):"))
        self.label_6.setText(_translate("boltDetectDlg", "检测合格率(%):"))
        self.groupBox_2.setTitle(_translate("boltDetectDlg", "控制参数"))
        self.label_12.setText(_translate("boltDetectDlg", "连续排除数(个):"))
        self.label_13.setText(_translate("boltDetectDlg", "吹气时间 (毫秒):"))
        self.label_14.setText(_translate("boltDetectDlg", "包装机联机状态:"))
        self.label_16.setText(_translate("boltDetectDlg", "包装数目(个):"))
