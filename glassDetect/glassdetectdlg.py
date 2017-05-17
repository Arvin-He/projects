# -*- coding:utf-8 -*-

import os
import sys
import time
from datetime import datetime
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QFileDialog, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
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
        self.plot()

    def plot(self):
        # data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        # ax.plot(data, 'r-')
        ax.set_title('玻璃边缘宽度值曲线')
        self.draw()


class GlassDetectDlg(QDialog, glassDetectDlg):

    def __init__(self, parent=None):
        super(GlassDetectDlg, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.canvas = ImageCanvas(self, width=5, height=3)
        self.canvas.move(2, 399)

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
            src_resize = imgprocess.resizeImage(src)
            self.showImage(src_resize)

    def on_prevImage(self):
        global imageIndex
        if imageList:
            if imageIndex-1 < 0:
                imageIndex = len(imageList)
            imageIndex -= 1
            src = imgprocess.loadImage(imageList[imageIndex])
            src_resize = imgprocess.resizeImage(src)
            self.showImage(src_resize)

    def on_nextImage(self):
        global imageIndex
        if imageList:
            if imageIndex >= len(imageList):
                imageIndex = 0
            imageIndex += 1
            src = imgprocess.loadImage(imageList[imageIndex])
            src_resize = imgprocess.resizeImage(src)
            self.showImage(src_resize)


    def on_upLimitEdited(self):
        global upLimit
        upLimit = float(self.upLimitEdit.text())

    def on_downLimitEdited(self):
        global downLimit
        downLimit = float(self.downLimitEdit.text())

    def showImage(self, img):
        rgb_img = imgprocess.convertBGR2RGB(img)
        qimg = QImage(
            rgb_img.data, rgb_img.shape[1], rgb_img.shape[0], QImage.Format_RGB888)
        qpm = QPixmap.fromImage(qimg)
        self.imageViewLabel.setPixmap(qpm)

    def processImg(self):
        pass

    def showResult(self):
        pass
