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


class ImageCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        super(ImageCanvas, self).__init__(fig)
        # FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        # plt.figure(figsize=(20,10))
        fig.patch.set_facecolor("green")
        # FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()


class GlassDetectDlg(QDialog, glassDetectDlg):
    def __init__(self, parent=None):
        super(GlassDetectDlg, self).__init__(parent)
        global imageList
        self.setupUi(self)
        self.initUI()
        imageList = utils.getImageList(os.path.abspath(image_path))
        src = imgprocess.loadImage(imageList[0])
        src_resize = imgprocess.resizeImage(src)
        self.showImage(src_resize)
        # image_rect = self.imageViewLabel.rect()
        self.imageViewLabel.setGeometry(5, 5, src_resize.shape[1], src_resize.shape[0])
        self.canvas = ImageCanvas(self, width=5, height=3)
        self.canvas.move(5, 400)

    def initUI(self):
        imagePath = utils.read_config(_config_path, "param", "image_path")
        # self.imagePathEdit.setText(imagePath if imagePath else image_path)
        self.loadImagePathBtn.clicked.connect(self.on_loadImagePath)
        self.prevImgBtn.clicked.connect(self.on_prevImage)
        self.nextImgBtn.clicked.connect(self.on_nextImage)
        # self.paramSettingBtn.clicked.connect(self.on_setParamEnable)
        self.upLimitEdit.editingFinished.connect(self.on_upLimitEdited)
        self.downLimitEdit.editingFinished.connect(self.on_downLimitEdited)

    def on_loadImagePath(self):
        fileName, ok = QFileDialog.getOpenFileName(
            self,  "Select image", "", "Image Files (*.bmp);;All Files (*)")
        self.imagePathEdit.setText(fileName)
        image_path = os.path.dirname(fileName)
        utils.write_config(_config_path, "param", "image_path", image_path)
        print(image_path)
        global imageList
        if imageList:
            imageList.clear()
        imageList = utils.getImageList(image_path)
        print(imageList)

    def on_prevImage(self):
        pass

    def on_nextImage(self):
        pass

    def on_setParamEnable(self):
        self.upLimitEdit.setReadOnly(False)
        self.downLimitEdit.setReadOnly(False)

    def on_upLimitEdited(self):
        pass

    def on_downLimitEdited(self):
        pass

    def showImage(self, img):
        rgb_img = imgprocess.convertBGR2RGB(img)
        qimg = QImage(rgb_img.data, rgb_img.shape[1], rgb_img.shape[0], QImage.Format_RGB888)
        qpm = QPixmap.fromImage(qimg)
        self.imageViewLabel.setPixmap(qpm)
