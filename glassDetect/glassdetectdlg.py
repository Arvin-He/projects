# -*- coding:utf-8 -*-

import os
import sys
import time
from datetime import datetime
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
import utils
import imgprocess
from glassdetectdlg_ui import Ui_glassDetectDlg as glassDetectDlg

app = QtWidgets.QApplication(sys.argv)
_config_path = os.path.abspath("config.ini")
image_path = os.path.join(os.path.abspath("res"), "images")
imageList = []
imageIndex = 0
upLimit = 0.0
downLimit = 0.0


class ImageCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        super(ImageCanvas, self).__init__(fig)
        self.setParent(parent)
        fig.patch.set_facecolor("green")
        FigureCanvas.updateGeometry(self)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title('Glass boarder width')
        self.draw()

    def plot(self, x, y):
        self.ax.plot(x, y)
        self.draw()


class GlassDetectDlg(QDialog, glassDetectDlg):

    def __init__(self, parent=None):
        super(GlassDetectDlg, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.canvas = ImageCanvas(self, width=5, height=3)
        self.canvas.move(0, 399)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)

    def initUI(self):
        self.loadImagePathBtn.clicked.connect(self.on_loadImagePath)
        self.prevImgBtn.clicked.connect(self.on_prevImage)
        self.nextImgBtn.clicked.connect(self.on_nextImage)
        self.upLimitEdit.editingFinished.connect(self.on_upLimitEdited)
        self.downLimitEdit.editingFinished.connect(self.on_downLimitEdited)

    def on_loadImagePath(self):
        fileName, ok = QFileDialog.getOpenFileName(
            self, "Select image", "", "Image Files (*.bmp);;All Files (*)")
        image_path = os.path.dirname(fileName)
        utils.write_config(_config_path, "param", "image_path", image_path)
        global imageList
        if imageList:
            imageList.clear()
        imageList = utils.getImageList(image_path)

        global imageIndex
        for index, item in enumerate(imageList):
            if item == os.path.normpath(fileName):
                imageIndex = index
        if imageList:
            src = imgprocess.loadImage(imageList[imageIndex])
            src_resize = imgprocess.resizeImg(src)
            self.showImage(src_resize)
            self.showResult(src)

    def on_prevImage(self):
        global imageIndex, imageList
        if imageList:
            if imageIndex-1 < 0:
                imageIndex = len(imageList)
            imageIndex -= 1
            src = imgprocess.loadImage(imageList[imageIndex])
            src_resize = imgprocess.resizeImg(src)
            self.showImage(src_resize)

    def on_nextImage(self):
        global imageIndex, imageList
        if imageList:
            if imageIndex+1 >= len(imageList):
                imageIndex = 0
            imageIndex += 1
            src = imgprocess.loadImage(imageList[imageIndex])
            src_resize = imgprocess.resizeImg(src)
            self.showImage(src_resize)

    def on_upLimitEdited(self):
        global upLimit
        upLimit = float(self.upLimitEdit.text())

    def on_downLimitEdited(self):
        global downLimit
        downLimit = float(self.downLimitEdit.text())

    def showImage(self, img):
        src2 = imgprocess.resizeImg(img)
        rgb_img = imgprocess.convertBGR2RGB(src2)
        qimg = QImage(
            rgb_img.data, rgb_img.shape[1], rgb_img.shape[0], QImage.Format_RGB888)
        qpm = QPixmap.fromImage(qimg)
        self.imageViewLabel.setPixmap(qpm)

    def showResult(self, img):
        data = imgprocess.get_image_process_data(img)
        res = imgprocess.data_analysis(data)
        print(res)
        self.canvas.plot([row for row in range(data[0])], data[1])
        self.updateUI(res)

    def updateUI(self, data):
        self.minEdit.setText("{:.1f}".format(data["min"]))
        self.maxEdit.setText("{:.1f}".format(data["max"]))
        self.meanEdit.setText("{:.3f}".format(data["mean"]))
        self.diffEdit.setText("{:.3f}".format(data["diff"]))
        self.evaluateEdit.setText("{:.1f}".format(data["estimate"]))

    def judgeResult(self):
        pass

