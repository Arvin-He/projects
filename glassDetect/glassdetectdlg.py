# -*- coding:utf-8 -*-

import os
import sys
import time
from datetime import datetime
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog

import utils
from glassdetectdlg_ui import Ui_glassDetectDlg as glassDetectDlg

app = QtWidgets.QApplication(sys.argv)


class GlassDetectDlg(QDialog, glassDetectDlg):
    def __init__(self, parent=None):
        super(GlassDetectDlg, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        pass