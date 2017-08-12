# !/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtGui
from PyQt5 import QtCore, QtWidgets
from valueReader import MainWindow

app = QtWidgets.QApplication(sys.argv)

if __name__ == "__main__":
    mainWin = MainWindow()
    mainWinRect = mainWin.geometry()
    mainWin.setFixedSize(mainWinRect.size())
    mainWin.exec_()
