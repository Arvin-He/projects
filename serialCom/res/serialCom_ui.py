# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serialCom.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_serialDlg(object):
    def setupUi(self, serialDlg):
        serialDlg.setObjectName("serialDlg")
        serialDlg.resize(590, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(serialDlg.sizePolicy().hasHeightForWidth())
        serialDlg.setSizePolicy(sizePolicy)
        self.groupBox = QtWidgets.QGroupBox(serialDlg)
        self.groupBox.setGeometry(QtCore.QRect(20, 140, 541, 251))
        self.groupBox.setObjectName("groupBox")
        self.recvHexEdit = QtWidgets.QLineEdit(self.groupBox)
        self.recvHexEdit.setGeometry(QtCore.QRect(130, 40, 380, 30))
        self.recvHexEdit.setReadOnly(True)
        self.recvHexEdit.setObjectName("recvHexEdit")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 40, 110, 30))
        self.label.setObjectName("label")
        self.transValEdit = QtWidgets.QLineEdit(self.groupBox)
        self.transValEdit.setGeometry(QtCore.QRect(130, 90, 150, 30))
        self.transValEdit.setReadOnly(True)
        self.transValEdit.setObjectName("transValEdit")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 110, 30))
        self.label_2.setObjectName("label_2")
        self.tightTorqueEdit = QtWidgets.QLineEdit(self.groupBox)
        self.tightTorqueEdit.setGeometry(QtCore.QRect(130, 140, 150, 30))
        self.tightTorqueEdit.setReadOnly(True)
        self.tightTorqueEdit.setObjectName("tightTorqueEdit")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 110, 30))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(290, 140, 60, 30))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(290, 190, 110, 30))
        self.label_6.setObjectName("label_6")
        self.tightAngleEdit = QtWidgets.QLineEdit(self.groupBox)
        self.tightAngleEdit.setGeometry(QtCore.QRect(130, 190, 150, 30))
        self.tightAngleEdit.setReadOnly(True)
        self.tightAngleEdit.setObjectName("tightAngleEdit")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 190, 111, 31))
        self.label_4.setObjectName("label_4")
        self.groupBox_2 = QtWidgets.QGroupBox(serialDlg)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 10, 541, 111))
        self.groupBox_2.setObjectName("groupBox_2")
        self.openBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.openBtn.setGeometry(QtCore.QRect(310, 20, 100, 30))
        self.openBtn.setObjectName("openBtn")
        self.portEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.portEdit.setGeometry(QtCore.QRect(120, 20, 150, 30))
        self.portEdit.setReadOnly(False)
        self.portEdit.setObjectName("portEdit")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(20, 20, 110, 30))
        self.label_7.setObjectName("label_7")
        self.closeBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.closeBtn.setGeometry(QtCore.QRect(310, 60, 100, 30))
        self.closeBtn.setObjectName("closeBtn")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(20, 60, 110, 30))
        self.label_8.setObjectName("label_8")
        self.baudrateEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.baudrateEdit.setGeometry(QtCore.QRect(120, 60, 150, 30))
        self.baudrateEdit.setReadOnly(False)
        self.baudrateEdit.setObjectName("baudrateEdit")
        self.stopReadBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.stopReadBtn.setGeometry(QtCore.QRect(420, 60, 100, 30))
        self.stopReadBtn.setObjectName("stopReadBtn")
        self.startReadBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.startReadBtn.setGeometry(QtCore.QRect(420, 20, 100, 30))
        self.startReadBtn.setObjectName("startReadBtn")
        self.infoLabel = QtWidgets.QLabel(serialDlg)
        self.infoLabel.setGeometry(QtCore.QRect(20, 410, 541, 30))
        self.infoLabel.setText("")
        self.infoLabel.setObjectName("infoLabel")

        self.retranslateUi(serialDlg)
        QtCore.QMetaObject.connectSlotsByName(serialDlg)

    def retranslateUi(self, serialDlg):
        _translate = QtCore.QCoreApplication.translate
        serialDlg.setWindowTitle(_translate("serialDlg", "Value Reader"))
        self.groupBox.setTitle(_translate("serialDlg", "数据信息:"))
        self.label.setText(_translate("serialDlg", "接收信息(Hex):"))
        self.label_2.setText(_translate("serialDlg", "整合数值(int):"))
        self.label_3.setText(_translate("serialDlg", "拧紧力矩(float):"))
        self.label_5.setText(_translate("serialDlg", "N.m"))
        self.label_6.setText(_translate("serialDlg", "degree"))
        self.label_4.setText(_translate("serialDlg", "拧紧角度(int):"))
        self.groupBox_2.setTitle(_translate("serialDlg", "串口设置:"))
        self.openBtn.setText(_translate("serialDlg", "打开串口"))
        self.label_7.setText(_translate("serialDlg", "COM端口:"))
        self.closeBtn.setText(_translate("serialDlg", "关闭串口"))
        self.label_8.setText(_translate("serialDlg", "波特率:"))
        self.stopReadBtn.setText(_translate("serialDlg", "停止读取"))
        self.startReadBtn.setText(_translate("serialDlg", "开始读取"))
