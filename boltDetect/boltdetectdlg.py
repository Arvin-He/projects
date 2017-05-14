# -*- coding:utf-8 -*-

import os
import sys
import time
from datetime import datetime
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog

import utils
from boltdetect_ui import Ui_boltDetectDlg as boltDetectDlg

app = QtWidgets.QApplication(sys.argv)


class BoltDetectDlg(QDialog, boltDetectDlg):
    def __init__(self, parent=None):
        super(BoltDetectDlg, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        pass