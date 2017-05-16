# -*- coding:utf-8 -*-

import os
import sys
import time
from datetime import datetime
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtGui import QImage, QPixmap

import utils
import imgprocess
from glassdetectdlg_ui import Ui_glassDetectDlg as glassDetectDlg

app = QtWidgets.QApplication(sys.argv)
_config_path = os.path.abspath("config.ini")
image_path = os.path.join(os.path.abspath("res"), "images")
imageList = []


class GlassDetectDlg(QDialog, glassDetectDlg):
    def __init__(self, parent=None):
        super(GlassDetectDlg, self).__init__(parent)
        global imageList
        self.setupUi(self)
        self.initUI()
        imageList = utils.getImageList(os.path.abspath(self.imagePathEdit.text()))
        print(imageList)
        src = imgprocess.loadImage(imageList[0])
        self.showImage(src)

    def initUI(self):
        imagePath = utils.read_config(_config_path, "param", "image_path")
        self.imagePathEdit.setText(imagePath if imagePath else image_path)
        self.loadImagePathBtn.clicked.connect(self.on_loadImagePath)
        self.prevImgBtn.clicked.connect(self.on_prevImage)
        self.nextImgBtn.clicked.connect(self.on_nextImage)
        self.paramSettingBtn.clicked.connect(self.on_setParamEnable)
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
