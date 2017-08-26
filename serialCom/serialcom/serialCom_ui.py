# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\projects\serialCom\serialcom\res\serialcom.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_serialDlg(object):
    def setupUi(self, serialDlg):
        serialDlg.setObjectName("serialDlg")
        serialDlg.resize(1024, 768)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(serialDlg.sizePolicy().hasHeightForWidth())
        serialDlg.setSizePolicy(sizePolicy)
        self.groupBox = QtWidgets.QGroupBox(serialDlg)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 541, 281))
        self.groupBox.setObjectName("groupBox")
        self.recvHexEdit = QtWidgets.QLineEdit(self.groupBox)
        self.recvHexEdit.setGeometry(QtCore.QRect(130, 30, 391, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.recvHexEdit.setFont(font)
        self.recvHexEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.recvHexEdit.setReadOnly(True)
        self.recvHexEdit.setObjectName("recvHexEdit")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 30, 110, 35))
        self.label.setObjectName("label")
        self.transValEdit = QtWidgets.QLineEdit(self.groupBox)
        self.transValEdit.setGeometry(QtCore.QRect(130, 80, 150, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.transValEdit.setFont(font)
        self.transValEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.transValEdit.setReadOnly(True)
        self.transValEdit.setObjectName("transValEdit")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 110, 35))
        self.label_2.setObjectName("label_2")
        self.tightTorqueEdit = QtWidgets.QLineEdit(self.groupBox)
        self.tightTorqueEdit.setGeometry(QtCore.QRect(130, 130, 150, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.tightTorqueEdit.setFont(font)
        self.tightTorqueEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tightTorqueEdit.setReadOnly(True)
        self.tightTorqueEdit.setObjectName("tightTorqueEdit")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 130, 110, 35))
        self.label_3.setObjectName("label_3")
        self.tightAngleEdit = QtWidgets.QLineEdit(self.groupBox)
        self.tightAngleEdit.setGeometry(QtCore.QRect(130, 180, 150, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.tightAngleEdit.setFont(font)
        self.tightAngleEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tightAngleEdit.setReadOnly(True)
        self.tightAngleEdit.setObjectName("tightAngleEdit")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 180, 105, 35))
        self.label_4.setObjectName("label_4")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(20, 230, 110, 35))
        self.label_10.setObjectName("label_10")
        self.flagBitEdit = QtWidgets.QLineEdit(self.groupBox)
        self.flagBitEdit.setGeometry(QtCore.QRect(130, 230, 151, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.flagBitEdit.setFont(font)
        self.flagBitEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.flagBitEdit.setReadOnly(True)
        self.flagBitEdit.setObjectName("flagBitEdit")
        self.flagBitLabel = QtWidgets.QLabel(self.groupBox)
        self.flagBitLabel.setGeometry(QtCore.QRect(290, 230, 40, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.flagBitLabel.setFont(font)
        self.flagBitLabel.setStyleSheet("color: rgb(0, 255, 0);\n"
"background-color: rgb(0, 0, 0);")
        self.flagBitLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.flagBitLabel.setObjectName("flagBitLabel")
        self.groupBox_2 = QtWidgets.QGroupBox(serialDlg)
        self.groupBox_2.setGeometry(QtCore.QRect(570, 10, 440, 175))
        self.groupBox_2.setObjectName("groupBox_2")
        self.openBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.openBtn.setGeometry(QtCore.QRect(210, 30, 100, 40))
        self.openBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.openBtn.setAutoDefault(False)
        self.openBtn.setObjectName("openBtn")
        self.portEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.portEdit.setGeometry(QtCore.QRect(80, 32, 120, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.portEdit.setFont(font)
        self.portEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.portEdit.setReadOnly(False)
        self.portEdit.setObjectName("portEdit")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(10, 30, 65, 35))
        self.label_7.setObjectName("label_7")
        self.closeBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.closeBtn.setGeometry(QtCore.QRect(210, 80, 100, 40))
        self.closeBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.closeBtn.setAutoDefault(False)
        self.closeBtn.setObjectName("closeBtn")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(10, 80, 65, 35))
        self.label_8.setObjectName("label_8")
        self.baudrateEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.baudrateEdit.setGeometry(QtCore.QRect(80, 82, 120, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.baudrateEdit.setFont(font)
        self.baudrateEdit.setReadOnly(False)
        self.baudrateEdit.setObjectName("baudrateEdit")
        self.stopReadBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.stopReadBtn.setGeometry(QtCore.QRect(330, 80, 100, 40))
        self.stopReadBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.stopReadBtn.setAutoDefault(False)
        self.stopReadBtn.setObjectName("stopReadBtn")
        self.startReadBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.startReadBtn.setGeometry(QtCore.QRect(330, 30, 100, 40))
        self.startReadBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.startReadBtn.setAutoDefault(False)
        self.startReadBtn.setObjectName("startReadBtn")
        self.infoLabel = QtWidgets.QLabel(self.groupBox_2)
        self.infoLabel.setGeometry(QtCore.QRect(10, 130, 420, 35))
        self.infoLabel.setObjectName("infoLabel")
        self.groupBox_3 = QtWidgets.QGroupBox(serialDlg)
        self.groupBox_3.setGeometry(QtCore.QRect(570, 200, 441, 91))
        self.groupBox_3.setObjectName("groupBox_3")
        self.barcodeEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.barcodeEdit.setGeometry(QtCore.QRect(80, 30, 350, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.barcodeEdit.setFont(font)
        self.barcodeEdit.setReadOnly(False)
        self.barcodeEdit.setObjectName("barcodeEdit")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(10, 30, 65, 40))
        self.label_5.setObjectName("label_5")
        self.groupBox_4 = QtWidgets.QGroupBox(serialDlg)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 300, 991, 451))
        self.groupBox_4.setObjectName("groupBox_4")
        self.groupCountEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.groupCountEdit.setGeometry(QtCore.QRect(110, 30, 120, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.groupCountEdit.setFont(font)
        self.groupCountEdit.setObjectName("groupCountEdit")
        self.preBtn = QtWidgets.QPushButton(self.groupBox_4)
        self.preBtn.setGeometry(QtCore.QRect(690, 20, 120, 50))
        self.preBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.preBtn.setAutoDefault(False)
        self.preBtn.setObjectName("preBtn")
        self.nextBtn = QtWidgets.QPushButton(self.groupBox_4)
        self.nextBtn.setGeometry(QtCore.QRect(860, 20, 120, 50))
        self.nextBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.nextBtn.setAutoDefault(False)
        self.nextBtn.setObjectName("nextBtn")
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setGeometry(QtCore.QRect(20, 30, 85, 30))
        self.label_6.setObjectName("label_6")
        self.label_9 = QtWidgets.QLabel(self.groupBox_4)
        self.label_9.setGeometry(QtCore.QRect(240, 30, 100, 35))
        self.label_9.setObjectName("label_9")
        self.dataListPanel = QtWidgets.QListWidget(self.groupBox_4)
        self.dataListPanel.setGeometry(QtCore.QRect(20, 80, 421, 361))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.dataListPanel.setFont(font)
        self.dataListPanel.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dataListPanel.setObjectName("dataListPanel")
        self.productInfoPanel = QtWidgets.QListWidget(self.groupBox_4)
        self.productInfoPanel.setGeometry(QtCore.QRect(460, 80, 521, 361))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.productInfoPanel.setFont(font)
        self.productInfoPanel.setFocusPolicy(QtCore.Qt.NoFocus)
        self.productInfoPanel.setObjectName("productInfoPanel")
        self.currBtn = QtWidgets.QPushButton(self.groupBox_4)
        self.currBtn.setGeometry(QtCore.QRect(470, 20, 120, 50))
        self.currBtn.setAutoDefault(False)
        self.currBtn.setObjectName("currBtn")

        self.retranslateUi(serialDlg)
        QtCore.QMetaObject.connectSlotsByName(serialDlg)

    def retranslateUi(self, serialDlg):
        _translate = QtCore.QCoreApplication.translate
        serialDlg.setWindowTitle(_translate("serialDlg", "Value Reader"))
        self.groupBox.setTitle(_translate("serialDlg", "数据信息:"))
        self.label.setText(_translate("serialDlg", "接收信息(Hex):"))
        self.label_2.setText(_translate("serialDlg", "整合数值(int):"))
        self.label_3.setText(_translate("serialDlg", "拧紧力矩(N.m):"))
        self.label_4.setText(_translate("serialDlg", "拧紧角度(度):"))
        self.label_10.setText(_translate("serialDlg", "拧紧状态:"))
        self.flagBitLabel.setText(_translate("serialDlg", "OK"))
        self.groupBox_2.setTitle(_translate("serialDlg", "串口设置:"))
        self.openBtn.setText(_translate("serialDlg", "打开串口"))
        self.label_7.setText(_translate("serialDlg", "COM端口:"))
        self.closeBtn.setText(_translate("serialDlg", "关闭串口"))
        self.label_8.setText(_translate("serialDlg", "波特率:"))
        self.stopReadBtn.setText(_translate("serialDlg", "停止读取"))
        self.startReadBtn.setText(_translate("serialDlg", "开始读取"))
        self.infoLabel.setText(_translate("serialDlg", "信息:"))
        self.groupBox_3.setTitle(_translate("serialDlg", "条形码扫描:"))
        self.label_5.setText(_translate("serialDlg", "条形码:"))
        self.groupBox_4.setTitle(_translate("serialDlg", "数据显示:"))
        self.preBtn.setText(_translate("serialDlg", "查看上一组"))
        self.nextBtn.setText(_translate("serialDlg", "查看下一组"))
        self.label_6.setText(_translate("serialDlg", "设置螺丝分组:"))
        self.label_9.setText(_translate("serialDlg", "( 个 / 组 )"))
        self.currBtn.setText(_translate("serialDlg", "查看最新数据"))

