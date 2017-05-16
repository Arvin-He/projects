# __init__.py
from . import res_rc
res_rc

from PyQt5 import QtCore
from PyQt5 import QtWidgets

translator = QtCore.QTranslator()
translator.load(QtCore.QLocale(), "", "",
                ":/{}/translations".format(__name__.replace(".", "/")))
QtWidgets.qApp.installTranslator(translator)

from . import ccdview
ccdview

from . import ccdctrldlg
ccdctrldlg

from . import utils
utils



#ccdview.py
import logging
import os
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPainter, QColor, QPalette
from PyQt5.QtCore import QPoint, Qt
from .findModelAgain import findModelAgainDlg
import basic
from basic import R, F, P, unit
import _cnc

_logger = logging.getLogger(__name__)
_translate = QtCore.QCoreApplication.translate

# 全局信号
updateViewSignal = basic.Signal()

def showGrabFailedMessage(error_code):
    basic.showOkDialog(_translate("ccdview", "Grab image failed.\n{}".format(_cnc.GetErrString(error_code))))

# 从底层C++类继承并实例化和重写虚函数
class CCDImageView(_cnc.CCcdImageView):
    calibrateFinishedSignal = QtCore.pyqtSignal(float, float)
    grabFailedSignal = QtCore.pyqtSignal(int)
    def __init__(self):
        super(CCDImageView, self).__init__()
        self.resolution = [0.0, 0.0]
        self.grabFailedSignal.connect(showGrabFailedMessage)

    # 重写C++里的虚函数
    def UpdateView(self):
        updateViewSignal.emit()

    def ProgramStart(self):
        pass

    def FindModelManual(self, data):
        findModelAgainDlg.showFindModelAgainDlgSignal.emit(data)

    def GrabFailed(self, error_code):
        self.grabFailedSignal.emit(error_code)

    def CalibrateFinished(self, resolutionX, resolutionY):
        self.resolution[0] = resolutionX
        self.resolution[1] = resolutionY
        self.calibrateFinishedSignal.emit(self.resolution[0], self.resolution[1])


ccdImageView = CCDImageView()
basic.registerCleanupFunction(ccdImageView.Destroy)


class CCDView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(CCDView, self).__init__(parent)
        ccdImageView.Create()
        self.setFocusPolicy(QtCore.Qt.StrongFocus) # 要设置focusPolicy,否则不会响应按键事件
        self.setContentsMargins(0, 0, 0, 0)
        self.setPalette(QPalette(QColor("#333")))  # 设置调色板的颜色
        self.setAutoFillBackground(True)  # 自动填充背景
        self.setMouseTracking(True)
        self.cursorPos = (0, 0)
        self.setCursor(QtCore.Qt.CrossCursor)
        self.cancelDrawTemplateRect = True
        self.isDrawTemplateRect = False
        self.saveImageAction = QtWidgets.QAction(_translate("ccdview", "Save Image"), self)
        self.saveImageAction.triggered.connect(self.on_saveImage)
        self.loadImageAction = QtWidgets.QAction(_translate("ccdview", "Load Image"), self)
        self.loadImageAction.triggered.connect(self.on_loadImage)
        self.releaseImageAction = QtWidgets.QAction(_translate("ccdview", "Release Image"), self)
        self.releaseImageAction.triggered.connect(self.on_releaseImage)

        updateViewSignal.connect(self.repaintImage)

    def keyPressEvent(self, event):
        if (event.modifiers() == Qt.ControlModifier) and (
                event.key() == Qt.Key_PageDown or event.key() == Qt.Key_Minus):
            ccdImageView.OutFrameZoomOutFast()
        elif (event.modifiers() == Qt.ControlModifier) and (
                event.key() == Qt.Key_PageUp or event.key() == Qt.Key_Plus):
            ccdImageView.OutFrameZoomInFast()
        elif event.key() == Qt.Key_PageDown or event.key() == Qt.Key_Minus:
            # _logger.info("PageDown or Minus key was pressed")
            ccdImageView.OutFrameZoomOut()
        elif event.key() == Qt.Key_PageUp or event.key() == Qt.Key_Plus:
            # _logger.info("PageUp or Plus key was pressed")
            ccdImageView.OutFrameZoomIn()
        elif event.key() == Qt.Key_Home:
            # _logger.info("Home key was pressed")
            ccdImageView.OutFrameZoomToMax()
        elif event.key() == Qt.Key_End:
            # _logger.info("End key was pressed")
            ccdImageView.OutFrameZoomToMin()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        ccdImageView.OnPaint(painter, self.rect(), QPoint(self.cursorPos[0], self.cursorPos[1]))

    def repaintImage(self):
        self.update()
        # self.repaint()  # 强制重绘

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # _logger.info("x:{}, y:{}".format(event.x(), event.y()))
            if ccdImageView.OnLButtonDown(QPoint(event.x(), event.y()),
                                          _cnc.CMvRealPoint(R[101]*unit.cnc2hmiLength,
                                                            R[102]*unit.cnc2hmiLength,
                                                            R[103]*unit.cnc2hmiLength)):
                if ccdImageView.GetCurrentOperationMode() == _cnc.CCD_OP_GRAB_MODEL:
                    basic.showCCDTemplateDlg(ccdImageView.GetModelMgr().GetModelCount() - 1)
        elif event.button() == QtCore.Qt.RightButton:
            ccdImageView.OnRButtonDown(QPoint(event.x(), event.y()),
                                       _cnc.CMvRealPoint(R[101]*unit.cnc2hmiLength,
                                                         R[102]*unit.cnc2hmiLength,
                                                         R[103]*unit.cnc2hmiLength))

    def mouseMoveEvent(self, event):
        self.cursorPos = (event.x(), event.y())
        if not self.hasFocus():
            self.setFocus()

    def enterEvent(self, event):
        ccdImageView.OnMouseEnter()

    def leaveEvent(self, event):
        ccdImageView.OnMouseLeave()

    def contextMenuEvent(self, event):
        context_menu = QtWidgets.QMenu()
        context_menu.setStyleSheet("font-family:Droid Sans Fallback")
        context_menu.addAction(self.saveImageAction)
        context_menu.addAction(self.loadImageAction)
        context_menu.addAction(self.releaseImageAction)
        context_menu.exec_(event.globalPos())

    def on_saveImage(self):
        img = _cnc.CMvImage()
        ccdImageView.GrabFrame(img)
        save_path = os.path.join(basic.userDir, "image")
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        fileName, ok = QFileDialog.getSaveFileName(self, "保存图片", save_path,  "All Files (*);;Image Files (*.bmp)")
        if fileName:
            img.Save(fileName)

    def on_loadImage(self):
        save_path = os.path.join(basic.userDir, "image")
        if not os.path.exists(save_path):
            _logger.error(_translate("ccdview", "no such directory."))
            return
        fileName, fileType = QFileDialog.getOpenFileName(self, "选择图片", save_path, "Select Files (*.bmp)")
        if fileName:
            # _logger.info(fileName)
            ccdImageView.LoadTestImage(fileName)

    def on_releaseImage(self):
        ccdImageView.ReleaseTestImage()

# 为实现view窗口可以有滚动条,添加frame这个类,将view放在这个frame中
class CCDViewFrame(QtWidgets.QFrame):

    def __init__(self, parent=None):
        super(CCDViewFrame, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.hBox = QtWidgets.QHBoxLayout()
        self.hBox.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QtWidgets.QScrollArea()
        self.hBox.addWidget(self.scrollArea)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.scrollArea.setWidgetResizable(True)
        self.ccd_view = CCDView(self)
        self.scrollArea.setWidget(self.ccd_view)
        self.setLayout(self.hBox)
        self.setFixedSize(500, 500)

    def adjustCCDViewSize(self, width, height):
        # self.ccd_view.resize(width, height) # 这个不管用
        self.ccd_view.setFixedSize(width, height)
        # _logger.info("resize = {}/{}".format(width, height))

    def contextMenuEvent(self, event):
        context_menu = QtWidgets.QMenu()
        context_menu.setStyleSheet("font-family:Droid Sans Fallback")
        context_menu.addAction(self.saveImageAction)
        context_menu.addAction(self.loadImageAction)


ccd_view_frame = CCDViewFrame(basic.mainWindow)


# ccdTemplateBase.py
# DIYTemplateSizeDlg 和 SetSearchRangeDlg大部分功能基本一致,故提取公共部分为基类
# 不同部分分别在子类中实现,达到代码重复利用.
import logging
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QRubberBand
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QRect, QPoint
from .ccdview import ccdImageView
from common.widgets.integerLineEdit import PyIntegerLineEdit

import basic
import _cnc

_logger = logging.getLogger(__name__)
_translate = QtCore.QCoreApplication.translate

class TemplateImage(QLabel):

    def __init__(self, parent=None):
        super(TemplateImage, self).__init__(parent)
        self.setStyleSheet("background-color:#333")
        self.setAlignment(Qt.AlignCenter)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.drawGrabImage(painter)
        painter.end()

    def drawGrabImage(self, painter):
        image = _cnc.CMvImage()
        status = ccdImageView.GrabFrame(image)
        if status == _cnc.CCD_ERR_OK:
            painter.drawImage(self.rect(), _cnc.CQImage(image))
        else:
            _logger.error(_translate("ccdTemplateBase", "Grab image error:{}").format(_cnc.GetErrString(status)))


class TemplateRect(QLabel):
    templateSizeChangedSignal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(TemplateRect, self).__init__(parent)
        self.setStyleSheet("background:transparent")
        self.setAlignment(Qt.AlignCenter)
        self.setMouseTracking(True)
        self.templateRect = QRect(0, 0, 0, 0) # 模板矩形框
        self.rubber = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.leftBtnDown = False

    def mousePressEvent(self, event):
        self.xOffset = event.x() - self.templateRect.left()
        self.yOffset = event.y() - self.templateRect.top()
        if event.button() == Qt.LeftButton:
            self.leftBtnDown = True
            self.origin = event.pos()
        elif event.button() == Qt.RightButton:
            self.templateRect.setRect(0, 0, 0, 0)
            self.rubber.setGeometry(self.templateRect)
            self.templateSizeChangedSignal.emit()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rubber.show()
            self.leftBtnDown = False

    def mouseMoveEvent(self, event):
        if event.x() in range(self.templateRect.left()-15, self.templateRect.left()+15) and \
                        event.y() in range(self.templateRect.top()+15, self.templateRect.bottom()-15):
            self.setCursor(Qt.SizeHorCursor)
            if self.leftBtnDown:
                self.templateRect.setLeft(event.x())
                self.rubber.setGeometry(self.templateRect.normalized())
        elif event.x() in range(self.templateRect.right()-15, self.templateRect.right()+15) and \
                        event.y() in range(self.templateRect.top()+15, self.templateRect.bottom()-15):
            self.setCursor(Qt.SizeHorCursor)
            if self.leftBtnDown:
                self.templateRect.setRight(event.x())
                self.rubber.setGeometry(self.templateRect.normalized())
        elif event.x() in range(self.templateRect.left()+15, self.templateRect.right()-15) and \
                        event.y() in range(self.templateRect.top()-15, self.templateRect.top()+15):
            self.setCursor(Qt.SizeVerCursor)
            if self.leftBtnDown:
                self.templateRect.setTop(event.y())
                self.rubber.setGeometry(self.templateRect.normalized())
        elif event.x() in range(self.templateRect.left()+15, self.templateRect.right()-15) and \
                        event.y() in range(self.templateRect.bottom()-15, self.templateRect.bottom()+15):
            self.setCursor(Qt.SizeVerCursor)
            if self.leftBtnDown:
                self.templateRect.setBottom(event.y())
                self.rubber.setGeometry(self.templateRect.normalized())
        elif event.x() in range(self.templateRect.left()-15, self.templateRect.left()+15) and \
                        event.y() in range(self.templateRect.top()-15, self.templateRect.top()+15):
            self.setCursor(Qt.SizeFDiagCursor)
            if self.leftBtnDown:
                self.templateRect.setTopLeft(event.pos())
                self.rubber.setGeometry(self.templateRect.normalized())
        elif event.x() in range(self.templateRect.left()-15, self.templateRect.left()+15) and \
                        event.y() in range(self.templateRect.bottom()-15, self.templateRect.bottom()+15):
            self.setCursor(Qt.SizeBDiagCursor)
            if self.leftBtnDown:
                self.templateRect.setBottomLeft(event.pos())
                self.rubber.setGeometry(self.templateRect.normalized())
        elif event.x() in range(self.templateRect.right()-15, self.templateRect.right()+15) and \
                        event.y() in range(self.templateRect.bottom()-15, self.templateRect.bottom()+15):
            self.setCursor(Qt.SizeFDiagCursor)
            if self.leftBtnDown:
                self.templateRect.setBottomRight(event.pos())
                self.rubber.setGeometry(self.templateRect.normalized())
        elif event.x() in range(self.templateRect.right()-15, self.templateRect.right()+15) and \
                        event.y() in range(self.templateRect.top()-15, self.templateRect.top()+15):
            self.setCursor(Qt.SizeBDiagCursor)
            if self.leftBtnDown:
                self.templateRect.setTopRight(event.pos())
                self.rubber.setGeometry(self.templateRect.normalized())
        elif event.x() in range(self.templateRect.left()+15, self.templateRect.right()-15) and \
                        event.y() in range(self.templateRect.top()+15, self.templateRect.bottom()-15):
            self.setCursor(Qt.SizeAllCursor)
            if self.leftBtnDown:
                self.templateRect.setRect(event.x() - self.xOffset, event.y() - self.yOffset,
                                        self.templateRect.width(), self.templateRect.height())
                self.rubber.setGeometry(self.templateRect.normalized())
        else:
            self.setCursor(Qt.ArrowCursor)
            if self.leftBtnDown:
                self.templateRect.setRect(self.origin.x(), self.origin.y(), abs(event.x()-self.origin.x()), abs(event.y()-self.origin.y()))
                self.rubber.setGeometry(self.templateRect.normalized())
        self.templateSizeChangedSignal.emit()

# 显示模板对话框的基类
class TemplateBaseDlg(QDialog):

    def __init__(self, parent=None):
        super(TemplateBaseDlg, self).__init__(parent)
        self.initUi()
        self.OKBtn.clicked.connect(self.on_OK)
        self.CancelBtn.clicked.connect(self.on_Cancel)
        self.myTemplateRect.templateSizeChangedSignal.connect(self.updateRectSize)

    def initUi(self):
        aoiRect = ccdImageView.GetAoi() # 获取图像尺寸
        self.imageRect = QRect(2, 2, aoiRect.width, aoiRect.height)
        self.dialogRect = QRect(0, 0, self.imageRect.width()+120, self.imageRect.height()+5) # 窗口尺寸
        self.myTemplateImage = TemplateImage(self) # 模板图像尺寸
        self.myTemplateImage.setGeometry(self.imageRect)
        self.myTemplateRect = TemplateRect(self)
        self.myTemplateRect.setGeometry(self.imageRect)
        defaultTemplateSize = ccdImageView.GetModelSize(_cnc.MODEL_SIZE_USER)
        self.myTemplateRect.templateRect = QRect((self.imageRect.width() - defaultTemplateSize.width) / 2,
                                                 (self.imageRect.height() - defaultTemplateSize.height) / 2,
                                                 defaultTemplateSize.width, defaultTemplateSize.height)
        self.myTemplateRect.rubber.setGeometry(self.myTemplateRect.templateRect)
        self.myTemplateRect.rubber.show()

        self.xLabel = QLabel("x Pos:", self)
        self.xLabel.setGeometry(self.imageRect.width()+10, self.dialogRect.top()+5, 100, 30)
        self.xPosEdit = PyIntegerLineEdit(self)
        self.xPosEdit.setGeometry(self.imageRect.width()+10, self.dialogRect.top()+35, 100, 30)
        self.xPosEdit.editingFinished.connect(self.on_modifyXPos)

        self.yLabel = QLabel("y Pos:", self)
        self.yLabel.setGeometry(self.imageRect.width()+10, self.dialogRect.top()+70, 100, 30)
        self.yPosEdit = PyIntegerLineEdit(self)
        self.yPosEdit.setGeometry(self.imageRect.width()+10, self.dialogRect.top()+100, 100, 30)
        self.yPosEdit.editingFinished.connect(self.on_modifyYPos)

        self.widthLabel = QLabel("Rect Width:", self)
        self.widthLabel.setGeometry(self.imageRect.width()+10, self.dialogRect.top()+135, 100, 30)
        self.widthEdit = PyIntegerLineEdit(self)
        self.widthEdit.setGeometry(self.imageRect.width()+10, self.dialogRect.top()+165, 100, 30)
        self.widthEdit.editingFinished.connect(self.on_modifyRectWidth)

        self.heightLabel = QLabel("Rect Height:", self)
        self.heightLabel.setGeometry(self.imageRect.width()+10, self.dialogRect.top()+200, 100, 30)
        self.heightEdit = PyIntegerLineEdit(self)
        self.heightEdit.setGeometry(self.imageRect.width()+10, self.dialogRect.top()+230, 100, 30)
        self.heightEdit.editingFinished.connect(self.on_modifyRectHeight)

        self.imageWidthLabel = QLabel("Image Width:", self)
        self.imageWidthLabel.setGeometry(self.imageRect.width() + 10, self.dialogRect.top() + 265, 100, 30)
        self.imageWidthEdit = PyIntegerLineEdit(self)
        self.imageWidthEdit.setGeometry(self.imageRect.width() + 10, self.dialogRect.top() + 295, 100, 30)
        self.imageWidthEdit.setReadOnly(True)

        self.imageHeightLabel = QLabel("Image Height:", self)
        self.imageHeightLabel.setGeometry(self.imageRect.width() + 10, self.dialogRect.top() + 330, 100, 30)
        self.imageHeightEdit = PyIntegerLineEdit(self)
        self.imageHeightEdit.setGeometry(self.imageRect.width() + 10, self.dialogRect.top() + 360, 100, 30)
        self.imageHeightEdit.setReadOnly(True)

        self.xPosEdit.setValue((self.imageRect.width() - defaultTemplateSize.width) / 2)
        self.yPosEdit.setValue((self.imageRect.height() - defaultTemplateSize.height) / 2)
        self.widthEdit.setValue(defaultTemplateSize.width)
        self.heightEdit.setValue(defaultTemplateSize.height)
        self.imageWidthEdit.setValue(self.imageRect.width())
        self.imageHeightEdit.setValue(self.imageRect.height())

        self.OKBtn = QtWidgets.QPushButton("OK", self)
        self.OKBtn.setGeometry(self.imageRect.width()+10, self.dialogRect.bottom()-80, 100, 30)
        self.CancelBtn = QtWidgets.QPushButton("Cancel", self)
        self.CancelBtn.setGeometry(self.imageRect.width()+10, self.dialogRect.bottom()-35, 100, 30)

        self.setGeometry(self.dialogRect)

    def updateRectSize(self):
        self.xPosEdit.setValue(self.myTemplateRect.templateRect.left())
        self.yPosEdit.setValue(self.myTemplateRect.templateRect.top())
        self.widthEdit.setValue(self.myTemplateRect.templateRect.width())
        self.heightEdit.setValue(self.myTemplateRect.templateRect.height())

    def on_modifyXPos(self):
        xPos = self.xPosEdit.value()
        if xPos in range(0, self.imageRect.width()):
            self.myTemplateRect.templateRect.setLeft(xPos)
            self.myTemplateRect.rubber.setGeometry(self.myTemplateRect.templateRect)
        else:
            _logger.warning(_translate("ccdTemplateBase", "x pos is out of range."))

    def on_modifyYPos(self):
        yPos = self.yPosEdit.value()
        if yPos in range(0, self.imageRect.height()):
            self.myTemplateRect.templateRect.setTop(yPos)
            self.myTemplateRect.rubber.setGeometry(self.myTemplateRect.templateRect)
        else:
            _logger.warning(_translate("ccdTemplateBase", "y pos is out of range."))

    def on_modifyRectWidth(self):
        rectWidth = self.widthEdit.value()
        xPos = self.xPosEdit.value()
        if rectWidth in range(0, self.imageRect.width()-xPos):
            self.myTemplateRect.templateRect.setWidth(rectWidth)
            self.myTemplateRect.rubber.setGeometry(self.myTemplateRect.templateRect)
        else:
            _logger.warning(_translate("ccdTemplateBase", "rect width is out of range."))

    def on_modifyRectHeight(self):
        rectHeight = self.heightEdit.value()
        yPos = self.yPosEdit.value()
        if rectHeight in range(0, self.imageRect.height() - yPos):
            self.myTemplateRect.templateRect.setHeight(rectHeight)
            self.myTemplateRect.rubber.setGeometry(self.myTemplateRect.templateRect)
        else:
            _logger.warning(_translate("ccdTemplateBase", "rect width is out of range."))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            return

    def on_OK(self):
        pass

    def on_Cancel(self):
        self.close()


class DIYTemplateSizeDlg(TemplateBaseDlg):

    def __init__(self, parent=None):
        super(DIYTemplateSizeDlg, self).__init__(parent)

    def initUi(self):
        super(DIYTemplateSizeDlg, self).initUi()
        self.setWindowTitle(_translate("ccdTemplateBase", "DIY Template Size Dialog"))

    def on_OK(self):
        rect_size = _cnc.CMvSize()
        rect_size.width = self.myTemplateRect.templateRect.width()
        rect_size.height = self.myTemplateRect.templateRect.height()
        ccdImageView.SetUserModelSize(rect_size)
        self.close()


def showDIYTemplateSizeDlg():
    basic.showWindow(DIYTemplateSizeDlg)


class SetSearchRangeDlg(TemplateBaseDlg):

    def __init__(self, parent=None):
        super(SetSearchRangeDlg, self).__init__(parent)
        self.setSearchRangeModify = _cnc.CCcdSettingsDlg()
        self.ccdParam = ccdImageView.GetCcdParam()

    def initUi(self):
        super(SetSearchRangeDlg, self).initUi()
        self.setWindowTitle(_translate("ccdTemplateBase", "Set Search Range Dialog"))

    def on_OK(self):
        self.ccdParam.rcROI.x = self.myTemplateRect.templateRect.left()
        self.ccdParam.rcROI.y = self.myTemplateRect.templateRect.top()
        self.ccdParam.rcROI.width = self.myTemplateRect.templateRect.width()
        self.ccdParam.rcROI.height = self.myTemplateRect.templateRect.height()
        self.setSearchRangeModify.SetCcdParamChanged(_cnc.CCD_PARAM_PARAMETER)
        self.close()


def showSetSearchRangeDlg():
    basic.showWindow(SetSearchRangeDlg)


# ccdtemplatedlg.py

import logging, os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QMenuBar, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from .ccdview import ccdImageView
from common.widgets import integerLineEdit
import basic
import _cnc

_logger = logging.getLogger(__name__)
_translate = QtCore.QCoreApplication.translate

# 模板图像中的十字线
class TemplateCross(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(TemplateCross, self).__init__(parent)
        self.setStyleSheet("background:transparent")
        self.setAlignment(QtCore.Qt.AlignCenter)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.drawCross(painter)
        painter.end()

    def drawCross(self, painter):
        pen = QPen(QtCore.Qt.blue, 1, QtCore.Qt.CustomDashLine)
        pen.setDashPattern([15, 5])
        painter.setPen(pen)
        painter.drawLine(self.rect().left(), self.rect().top()+self.rect().width()/2,
                         self.rect().left()+self.rect().width(), self.rect().top()+self.rect().width()/2)
        painter.drawLine(self.rect().left()+ self.rect().width() / 2, self.rect().top(),
                         self.rect().left() + self.rect().width()/2, self.rect().top() + self.rect().height())

class CCDTemplateDlg(QDialog):
    ccdTemplateDlgHiddenSignal = QtCore.pyqtSignal(int)
    ccdTemplateDlgSetHomeDoneSignal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(CCDTemplateDlg, self).__init__(parent)
        self.ui = basic.loadUi(self, ":/common/ccd/CCDtemplatedlg.ui")
        self.ccdTemplate = _cnc.CCcdModelDlg()
        self.templateProperty = {}
        self.initUi()
        self.crossImage = TemplateCross(self)

    def initUi(self):
        self.initMenuBar()
        self.ui.showTemplateLabel.setAlignment(QtCore.Qt.AlignCenter)  # 设置模板图像居中显示
        for item in [_translate("ccdtemplatedlg", "Corner"), _translate("ccdtemplatedlg", "Image")]:
            self.ui.templateTypeCombox.addItem(item)
        for item in [_translate("ccdtemplatedlg", "1-LeftBottom"), _translate("ccdtemplatedlg", "2-RightBottom"),
                     _translate("ccdtemplatedlg", "3-RightTop"), _translate("ccdtemplatedlg", "4-LeftTop")]:
            self.ui.cornerTypeCombox.addItem(item)
        self.ui.lastTemplateBtn.clicked.connect(self.on_getLastTemplate)
        self.ui.nextTemplateBtn.clicked.connect(self.on_getNextTemplate)
        self.ui.deleteTemplateBtn.clicked.connect(self.on_deleteTemplate)
        self.ui.findTemplateBtn.clicked.connect(self.on_findTemplate)
        self.ui.templateNumberEdit.editingFinished2.connect(self.on_setTemplateNo)
        self.ui.templateTypeCombox.currentTextChanged.connect(self.on_selectTemplateType)
        self.ui.cornerTypeCombox.currentTextChanged.connect(self.on_selectCornerType)
        self.ui.xOffsetEdit.editingFinished2.connect(self.on_setTemplateOffset)
        self.ui.yOffsetEdit.editingFinished2.connect(self.on_setTemplateOffset)
        self.ui.xPosEdit.editingFinished2.connect(self.on_setTemplateRefPos)
        self.ui.yPosEdit.editingFinished2.connect(self.on_setTemplateRefPos)
        self.ui.thredholdValueEdit.editingFinished2.connect(self.on_setTemplateThreshold)
        self.ui.allowedErrorEdit.editingFinished2.connect(self.on_setTemplateAllowError)
        self.ui.allowedAngleErrorEdit.editingFinished2.connect(self.on_setTemplateAllowAngleError)
        self.ui.tryGrabBtn.clicked.connect(self.on_tryGrab)
        self.ui.toPointPosBtn.clicked.connect(self.on_goToPointPos)
        self.ui.trainBtn.clicked.connect(self.on_trainTemplate)
        for radioBtn in [self.ui.none, self.ui.integerPt1, self.ui.integerPt2,
                         self.ui.singlePt1, self.ui.singlePt2]:
            radioBtn.clicked.connect(self.on_selectTemplateMark)
        self.ui.setCCDHomeBtn.clicked.connect(self.on_setCCDHome)
        self.ui.OKBtn.clicked.connect(self.on_OK)
        self.ui.CancelBtn.clicked.connect(self.on_Cancel)
        self.ui.ApplyBtn.clicked.connect(self.on_Apply)

    def initMenuBar(self):
        self.menuList = []
        self.menuBar = QMenuBar(self)
        for menu in [ _translate("ccdtemplatedlg", "&Operate"),
                      "-",
                      _translate("ccdtemplatedlg", "&Template")]:
            if menu != "-":
                menuItem = self.menuBar.addMenu(menu)
                self.menuList.append(menuItem)
            else:
                self.menuBar.addSeparator()
        for action in [ _translate("ccdtemplatedlg", "&Save"),  _translate("ccdtemplatedlg", "&Read"),
                        _translate("ccdtemplatedlg", "&Copy"),  _translate("ccdtemplatedlg", "&Undo")]:
            self.menuList[0].addAction(QAction(action, self))
        for action in [ _translate("ccdtemplatedlg", "&CopyLast"),
                        _translate("ccdtemplatedlg", "&CopyNext"),
                        _translate("ccdtemplatedlg", "&CopyAssign"),
                        "-",
                        _translate("ccdtemplatedlg", "&VerticalMirror"),
                        _translate("ccdtemplatedlg", "&HorizontalMirror"),
                        "-",
                        _translate("ccdtemplatedlg", "&LeftRotate90"),
                        _translate("ccdtemplatedlg", "&RightRotate90"),
                        "-",
                        _translate("ccdtemplatedlg","&CutTemplate")]:
            if action != "-":
                self.menuList[1].addAction(QAction(action, self))
            else:
                self.menuList[1].addSeparator()
        for i, actionEvent in enumerate([self.on_save, self.on_read, self.on_copy, self.on_undo]):
            self.menuList[0].actions()[i].triggered.connect(actionEvent)
        for i, actionEvent in enumerate([self.on_copyLast, self.on_copyNext, self.on_copyAssign, "-",
                                         self.on_verticalMirror, self.on_HorizontalMirror, "-",
                                         self.on_leftRotate90, self.on_rightRotate90, "-", self.on_cutTemplate]):
            if actionEvent != "-":
                self.menuList[1].actions()[i].triggered.connect(actionEvent)
        self.menuBar.setGeometry(0, 0, 505, 25)

    def updateMenuStatus(self):
        if self.sender() in self.menuList[1].actions():
            self.ui.ccdTemplateFrame.setEnabled(False)
        else:
            self.ui.ccdTemplateFrame.setEnabled(True)

    def on_save(self):
        _logger.debug("save action")
        templateDir = os.path.join(basic.userDir, "template")
        if not os.path.exists(templateDir):
            os.mkdir(templateDir)
        template = self.ccdTemplate.GetCurrentModel()
        if template:
            fileName, ok = QFileDialog.getSaveFileName(self,  _translate("ccdtemplatedlg", "Template Saves"),
                                    templateDir, "Image Files (*.bmp);;All Files (*)")
            self.ccdTemplate.SaveModelImage(fileName)
        else:
            _logger.warning(_translate("ccdtemplatedlg", "template is none, save template failed."))

    def on_read(self):
        _logger.debug("read action")
        templateDir = os.path.join(basic.userDir, "template")
        if not os.path.exists(templateDir):
            _logger.warning(_translate("ccdtemplatedlg", "template path doesn't exist"))
            return
        fileName, ok = QFileDialog.getOpenFileName(self,  _translate("ccdtemplatedlg", "Select Template"), templateDir,
                                    "Image Files (*.bmp);;All Files (*)")
        # _logger.info("file name = {}".format(fileName))
        self.ccdTemplate.ReadModelImage(fileName)
        self.showTemplate()

    def on_copy(self):
        _logger.debug("copy action")
        status = self.ccdTemplate.CopyModel()
        if status:
            _logger.info(_translate("ccdtemplatedlg", "copy template success"))
        else:
            _logger.warning(_translate("ccdtemplatedlg", "copy template failed"))

    def on_undo(self):
        _logger.debug("undo action")
        self.ccdTemplate.LoadModelByIndex(self.ccdTemplate.GetCurrentModelIndex())
        self.showTemplate()

    def on_copyLast(self):
        _logger.debug("copy last")
        if self.ccdTemplate.CanCopyImageFromPrev():
            self.ccdTemplate.CopyImageFromPrev()
            self.showTemplate()
        else:
            _logger.warning(_translate("ccdtemplatedlg", "can not copy last template"))

    def on_copyNext(self):
        _logger.debug("copy next")
        if self.ccdTemplate.CanCopyImageFromNext():
            self.ccdTemplate.CopyImageFromNext()
            self.showTemplate()
        else:
            _logger.warning("can not copy next template")

    def on_copyAssign(self):
        _logger.debug("Copy Assign")
        if self.ccdTemplate.CanCopyImage():
            if FindTemplateDlg.instance_count < 1:
                findTemplateDlg = FindTemplateDlg(self)
                findTemplateDlg.setWindowTitle(_translate("ccdtemplatedlg", "Copy Assign"))
                findTemplateDlg.titleLabel.setText(_translate("ccdtemplatedlg", "Please input template Index:"))
                findTemplateDlg.setGeometry(self.x() + self.width() / 2 - findTemplateDlg.width() / 2,
                                            self.y() + self.height() / 2 - findTemplateDlg.height() / 2,
                                            findTemplateDlg.width(),
                                            findTemplateDlg.height())
                findTemplateDlg.exec_()
                findTemplateDlg.destroy()

    def on_verticalMirror(self):
        _logger.debug("vertical mirror")
        self.ccdTemplate.ModelImageFlipVertical()
        self.showTemplate()

    def on_HorizontalMirror(self):
        _logger.debug("horizontal mirror")
        self.ccdTemplate.ModelImageFlipHorizontal()
        self.showTemplate()

    def on_leftRotate90(self):
        _logger.debug("leftRotate90")
        self.ccdTemplate.ModelImageRotateLeft90()
        self.showTemplate()

    def on_rightRotate90(self):
        _logger.debug("rightRotate90")
        self.ccdTemplate.ModelImageRotateRight90()
        self.showTemplate()

    def on_cutTemplate(self):
        _logger.debug("cutTemplate")
        self.ccdTemplate.ModelImageClip()
        self.showTemplate()

    def showTemplateByNo(self, template_no):
        if self.ccdTemplate.LoadModelByModelNo(template_no):
            template = self.ccdTemplate.GetCurrentModel()
            if template:
                self.getTemplateProperty(template)
                self.updateUI(template)

    # 显示模板图像,注意:界面上的index是从1开始
    def showTemplate(self, modelIndex=-1):
        if modelIndex >= 0:
            self.ccdTemplate.LoadModelByIndex(modelIndex)
        template = self.ccdTemplate.GetCurrentModel()
        if template:
            self.getTemplateProperty(template)
            self.updateUI(template)

    def updateUI(self, template):
        if template:
            self.ui.ccdTemplateFrame.setEnabled(True)
            self.ui.showTemplateLabel.setPixmap(QPixmap.fromImage(_cnc.CQImage(self.templateProperty["templateImage"])))
            self.crossImage.setGeometry(self.ui.showTemplateLabel.geometry())
            # current_index = self.ccdTemplate.GetCurrentModelIndex() 让sam修改下接口GetCurrentModelIndex() -> GetModelIndex()
            self.ui.templateIndex.setText("{}/{}".format(self.ccdTemplate.GetCurrentModelIndex() + 1,
                                                         self.ccdTemplate.GetModelCount()))
            self.ui.templateNumberEdit.setValue(self.templateProperty["templateNO"])
            self.ui.templateTypeCombox.setCurrentIndex(self.templateProperty["templateType"])
            self.ui.cornerTypeCombox.setCurrentIndex(self.templateProperty["templateCornerType"])
            self.ui.xOffsetEdit.setValue(self.templateProperty["templateOffset"].x)
            self.ui.yOffsetEdit.setValue(self.templateProperty["templateOffset"].y)
            self.ui.xPosEdit.setValue(self.templateProperty["templateRefPos"].x)
            self.ui.yPosEdit.setValue(self.templateProperty["templateRefPos"].y)
            self.ui.thredholdValueEdit.setValue(self.templateProperty["templateThreshold"])
            self.ui.allowedErrorEdit.setValue(self.templateProperty["templateOffsetMax"])
            self.ui.allowedAngleErrorEdit.setValue(self.templateProperty["templateAngleErrMax"])
            self.ui.discriberLabel.setText(self.templateProperty["templateDetails"])
            self.ui.trainInfoLabel.setText(_translate("ccdtemplatedlg", "trained") \
                                               if self.templateProperty["templateTrained"] else _translate("ccdtemplatedlg", "not trained"))
            if self.templateProperty["templateMark"] == _cnc.GRAB_NONE:
                self.ui.none.setChecked(True)
            elif self.templateProperty["templateMark"] == _cnc.GRAB_P1:
                self.ui.integerPt1.setChecked(True)
            elif self.templateProperty["templateMark"] == _cnc.GRAB_P2:
                self.ui.integerPt2.setChecked(True)
            elif self.templateProperty["templateMark"] == _cnc.GRAB_P3:
                self.ui.singlePt1.setChecked(True)
            elif self.templateProperty["templateMark"] == _cnc.GRAB_P4:
                self.ui.singlePt2.setChecked(True)
            if ccdImageView.GetCcdSetting(0).bUseLocPoint2:
                self.ui.singlePt2.setEnabled(True)
            else:
                self.ui.singlePt2.setEnabled(False)
        else:
            self.ui.showTemplateLabel.setPixmap(QPixmap.fromImage(QImage()))
            self.ui.templateIndex.setText("0/0")
            self.ui.ccdTemplateFrame.setEnabled(False)
            _logger.info(_translate("ccdtemplatedlg", "Template is none."))

    def getTemplateProperty(self, model):
        self.templateProperty["templateImage"] = model.m_ModelImage
        self.templateProperty["templateNO"] = model.m_nModelNo
        self.templateProperty["templateType"] = model.m_ModelProperty.nModelType
        self.templateProperty["templateCornerType"] = model.m_ModelProperty.nCornerType
        self.templateProperty["templateRefPos"] = model.m_ModelProperty.ptRefPos
        self.templateProperty["templateOffset"] = model.m_ModelProperty.ptOffset
        self.templateProperty["templateThreshold"] = model.m_ModelProperty.nThreshold
        self.templateProperty["templateOffsetMax"] = model.m_ModelProperty.nOffsetMax
        self.templateProperty["templateAngleErrMax"] = model.m_ModelProperty.nAngleErrMax
        self.templateProperty["templateDetails"] = model.m_ModelProperty.strDetails
        self.templateProperty["templateTrained"] = model.m_ModelProperty.bTrained
        self.templateProperty["templateMark"] = self.ccdTemplate.GetGrabPoint()

    def setTemplateProperty(self, model):
        model.m_ModelImage = self.templateProperty["templateImage"]
        model.m_nModelNo = self.templateProperty["templateNO"]
        model.m_ModelProperty.nModelType = self.templateProperty["templateType"]
        model.m_ModelProperty.nCornerType = self.templateProperty["templateCornerType"]
        model.m_ModelProperty.ptRefPos = self.templateProperty["templateRefPos"]
        model.m_ModelProperty.ptOffset = self.templateProperty["templateOffset"]
        model.m_ModelProperty.nThreshold = self.templateProperty["templateThreshold"]
        model.m_ModelProperty.nOffsetMax = self.templateProperty["templateOffsetMax"]
        model.m_ModelProperty.nAngleErrMax = self.templateProperty["templateAngleErrMax"]
        model.m_ModelProperty.strDetails = self.templateProperty["templateDetails"]
        model.m_ModelProperty.bTrained = self.templateProperty["templateTrained"]
        self.ccdTemplate.SetGrabPoint(self.templateProperty["templateMark"])

    def on_getLastTemplate(self):
        _logger.debug("get last template")
        if self.ccdTemplate.CanSelectPrevModel():
            self.ccdTemplate.SelectPrevModel()
            self.showTemplate()
            self.ui.showInfoLabel.setText("")
        else:
            _logger.warning(_translate("ccdtemplatedlg", "can not select prev model"))

    def on_getNextTemplate(self):
        _logger.debug("get next template")
        if self.ccdTemplate.CanSelectNextModel():
            self.ccdTemplate.SelectNextModel()
            self.showTemplate()
            self.ui.showInfoLabel.setText("")
        else:
            _logger.warning(_translate("ccdtemplatedlg", "can not select next model"))

    def on_deleteTemplate(self):
        _logger.debug("delete template")
        if self.ccdTemplate.CanDelModel():
            reply = basic.showOkCancelDialog(_translate("ccdtemplatedlg", "Delete this template?"))
            if reply == QMessageBox.Ok:
                self.ccdTemplate.DelModel()
                self.showTemplate()
                self.ui.showInfoLabel.setText("")
        else:
            _logger.warning(_translate("ccdtemplatedlg", "There is no template."))

    def on_findTemplate(self):
        _logger.debug("find template")
        if FindTemplateDlg.instance_count < 1:
            findTemplateDlg = FindTemplateDlg(self)
            findTemplateDlg.setGeometry(self.x() + self.width() / 2 - findTemplateDlg.width() / 2,
                                        self.y() + self.height() / 2 - findTemplateDlg.height() / 2,
                                        findTemplateDlg.width(),
                                        findTemplateDlg.height())
            findTemplateDlg.exec_()
            self.ui.showInfoLabel.setText("")
            findTemplateDlg.destroy()

    def on_setTemplateNo(self):
        self.templateProperty["templateNO"] = self.ui.templateNumberEdit.value()

    def on_selectTemplateType(self, text):
        _logger.debug("select template type")
        if text == _translate("ccdtemplatedlg", "Corner"):
            self.templateProperty["templateType"] = _cnc.ModelType_Corner
            self.ui.trainBtn.setEnabled(True)
        elif text == _translate("ccdtemplatedlg", "Image"):
            self.templateProperty["templateType"] = _cnc.ModelType_Image
            self.ui.trainBtn.setEnabled(False)
            self.ui.trainInfoLabel.setText("")

    def on_selectCornerType(self, text):
        _logger.debug("select corner type")
        if text == _translate("ccdtemplatedlg", "1-LeftBottom"):
            self.templateProperty["templateCornerType"] = _cnc.LeftBottom
        elif text == _translate("ccdtemplatedlg", "2-RightBottom"):
            self.templateProperty["templateCornerType"] = _cnc.RightBottom
        elif text == _translate("ccdtemplatedlg", "3-RightTop"):
            self.templateProperty["templateCornerType"] = _cnc.RightTop
        elif text == _translate("ccdtemplatedlg", "4-LeftTop"):
            self.templateProperty["templateCornerType"] = _cnc.LeftTop

    def on_setTemplateOffset(self, value):
        if self.sender() == self.ui.xOffsetEdit:
            self.templateProperty["templateOffset"] = _cnc.CMvRealPoint(value, self.ui.yOffsetEdit.value(), 0)
        elif self.sender() == self.ui.yOffsetEdit:
            self.templateProperty["templateOffset"] = _cnc.CMvRealPoint(self.ui.xOffsetEdit.value(), value, 0)

    def on_setTemplateRefPos(self, value):
        if self.sender() == self.ui.xPosEdit:
            self.templateProperty["templateRefPos"] = _cnc.CMvRealPoint(value, self.ui.yPosEdit.value(), 0)
        elif self.sender() == self.ui.yPosEdit:
            self.templateProperty["templateRefPos"] = _cnc.CMvRealPoint(self.ui.xPosEdit.value(), value, 0)

    def on_setTemplateThreshold(self):
        self.templateProperty["templateThreshold"] = self.ui.thredholdValueEdit.value()

    def on_setTemplateAllowError(self):
        self.templateProperty["templateOffsetMax"] = self.ui.allowedErrorEdit.value()

    def on_setTemplateAllowAngleError(self):
        self.templateProperty["templateAngleErrMax"] = self.ui.allowedAngleErrorEdit.value()

    def on_selectTemplateMark(self):
        _logger.debug("choose template mask")
        if self.sender() is self.ui.integerPt1:
            self.templateProperty["templateMark"] = 0
        elif self.sender() is self.ui.integerPt2:
            self.templateProperty["templateMark"] = 1
        elif self.sender() is self.ui.singlePt1:
            self.templateProperty["templateMark"] = 2
        elif self.sender() is self.ui.singlePt2:
            self.templateProperty["templateMark"] = 3
        elif self.sender() is self.ui.none:
            self.templateProperty["templateMark"] = 4

    def on_tryGrab(self):
        _logger.debug("try grab")
        if (self.ccdTemplate.TestFindModel()):
            result = ccdImageView.GetModelFindResult()
            self.ui.showInfoLabel.setText("template recognized success!\nScore:{:.1f}, ImagePos:({:.3f}, {:.3f})".format(
                    result.nScore, result.nXPosition, result.nYPosition))
        else:
            result = ccdImageView.GetModelFindResult()
            self.ui.showInfoLabel.setText("Template recognized failed!\nScore:{:.1f}".format(result.nScore))

    def on_goToPointPos(self):
        _logger.debug("go to point pos")
        ccdImageView.SetGotoModelPosition(self.templateProperty["templateNO"])
        basic.mdi('G65 P<CCD_GOTO_POINT>')

    def on_trainTemplate(self):
        _logger.debug("train template")
        if self.ccdTemplate.TrainModel():
            template = self.ccdTemplate.GetCurrentModel()
            self.getTemplateProperty(template)
            self.updateUI(template)

    def on_setCCDHome(self):
        _logger.debug("set as ccd home")
        self.ccdTemplate.SetAsCcdOrigin()
        self.ccdTemplateDlgSetHomeDoneSignal.emit()

    def hideEvent(self, event):
        if self.templateProperty["templateNO"]:
            self.ccdTemplateDlgHiddenSignal.emit(self.templateProperty["templateNO"])
        else:
            self.ccdTemplateDlgHiddenSignal.emit(0)

    def done(self, result):
        super(CCDTemplateDlg, self).done(result)
        ccdImageView.SetTrackTargetImage(False)

    def on_Apply(self):
        _logger.debug("click Apply btn")
        template = self.ccdTemplate.GetCurrentModel()
        if template:
            self.setTemplateProperty(template)
            self.ccdTemplate.ApplyChanges()
        else:
            _logger.error(_translate("ccdtemplatedlg", "There is no template!"))

    def on_OK(self):
        self.on_Apply()
        self.close()

    def on_Cancel(self):
        self.close()


ccdTemplateDlg = CCDTemplateDlg(basic.mainWindow)


class FindTemplateDlg(QDialog):
    instance_count = 0
    def __init__(self, parent=None):
        super(FindTemplateDlg, self).__init__(parent)
        FindTemplateDlg.instance_count += 1
        self.setWindowTitle(_translate("ccdtemplatedlg", "input"))
        self.titleLabel = QtWidgets.QLabel(_translate(
            "ccdtemplatedlg", "Please input template NO:"), self)
        self.titleLabel.setGeometry(50, 50, 200, 30)
        self.templateIndexEdit = integerLineEdit.PyIntegerLineEdit(self)
        self.templateIndexEdit.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.templateIndexEdit.setGeometry(50, 90, 350, 30)
        self.OKBtn = QtWidgets.QPushButton(
            _translate("ccdtemplatedlg", "OK"), self)
        self.OKBtn.setGeometry(190, 190, 100, 30)
        self.CancelBtn = QtWidgets.QPushButton(
            _translate("ccdtemplatedlg", "Cancel"), self)
        self.CancelBtn.setGeometry(300, 190, 100, 30)
        self.OKBtn.clicked.connect(self.on_OK)
        self.CancelBtn.clicked.connect(self.on_Cancel)
        self.setGeometry(basic.mainWindow.x() + (basic.mainWindow.width() - 450) / 2,
                         basic.mainWindow.y() + (basic.mainWindow.height() - 250) / 2,
                         450, 250)

    def showTemplateByNo(self, template_no):
        global ccdTemplateDlg
        if ccdTemplateDlg.ccdTemplate.LoadModelByModelNo(template_no):
            template = ccdTemplateDlg.ccdTemplate.GetCurrentModel()
            if template:
                ccdTemplateDlg.getTemplateProperty(template)
                ccdTemplateDlg.updateUI(template)

    def on_OK(self):
        global ccdTemplateDlg
        inputValue = self.templateIndexEdit.value()
        if inputValue <= 0:
            _logger.warning(_translate("ccdtemplatedlg", "please input a positive number"))
            self.templateIndexEdit.setValue(self.templateIndexEdit.lastValue)
            return
        else:
            if self.windowTitle() == "input":
                ccdTemplateDlg.showTemplateByNo(inputValue)
            elif self.windowTitle() == "Copy Assign":
                ccdTemplateDlg.ccdTemplate.CopyImageFrom(inputValue)
                ccdTemplateDlg.showTemplate()
            self.close()

    def on_Cancel(self):
        self.close()

    def done(self, result):
        super(FindTemplateDlg, self).done(result)
        FindTemplateDlg.instance_count -= 1


@basic.api
def showCCDTemplateDlg(model_index = -1):
    if ccdTemplateDlg.isVisible():
        ccdTemplateDlg.raise_()
        ccdTemplateDlg.activateWindow()
    else:
        geometry = ccdTemplateDlg.geometry()
        geometry.moveCenter(basic.mainWindow.geometry().center())
        ccdTemplateDlg.setGeometry(geometry)
        ccdTemplateDlg.show()
    ccdTemplateDlg.showTemplate(model_index)


# findModelAgain.py
import logging
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QPushButton, QLabel
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPen, QPainter
from common.widgets.integerLineEdit import PyIntegerLineEdit
import basic
import _cnc

_logger = logging.getLogger(__name__)
_translate = QtCore.QCoreApplication.translate

class TemplateRect(QLabel):
    templateRectPosChangedSignal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(TemplateRect, self).__init__(parent)
        self.setStyleSheet("background:transparent")
        self.setAlignment(Qt.AlignCenter)
        self.setMouseTracking(True)
        self.templateRect = QRect(0, 0, 0, 0) # 模板矩形框
        self.leftBtnDown = False
        self.drawRectPen = QPen(QtCore.Qt.blue, 1, QtCore.Qt.SolidLine)
        self.drawLinePen = QPen(QtCore.Qt.blue, 1, QtCore.Qt.DashLine)

    def drawTemplateRect(self, painter):
        painter.setPen(self.drawRectPen)
        painter.drawRect(self.templateRect)
        painter.setPen(self.drawLinePen)
        painter.drawLine(self.templateRect.left(), self.templateRect.top()+self.templateRect.height()/2,
                         self.templateRect.left()+self.templateRect.width(), self.templateRect.top()+self.templateRect.height()/2)
        painter.drawLine(self.templateRect.left()+self.templateRect.width()/2, self.templateRect.top(),
                         self.templateRect.left()+self.templateRect.width()/2, self.templateRect.top()+self.templateRect.height())

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.drawTemplateRect(painter)
        painter.end()

    def mousePressEvent(self, event):
        self.xOffset = event.x() - self.templateRect.left()
        self.yOffset = event.y() - self.templateRect.top()
        if event.button() == Qt.LeftButton:
            self.leftBtnDown = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftBtnDown = False

    def mouseMoveEvent(self, event):
        if self.templateRect.contains(event.pos()):
            self.setCursor(Qt.SizeAllCursor)
            if self.leftBtnDown:
                self.templateRect.setRect(event.x() - self.xOffset, event.y() - self.yOffset,
                                        self.templateRect.width(), self.templateRect.height())
                self.update()
                self.templateRectPosChangedSignal.emit()
        else:
            self.setCursor(Qt.ArrowCursor)


class AssistRecognizeDlg(QDialog):
    instance_count = 0
    def __init__(self, modelData, parent=None):
        super(AssistRecognizeDlg, self).__init__(parent)
        AssistRecognizeDlg.instance_count += 1
        self.modelData = modelData
        self.initUi()
        self.grabAgainBtn.clicked.connect(self.on_grabAgain)
        self.OKBtn.clicked.connect(self.on_OK)
        self.CancelBtn.clicked.connect(self.on_Cancel)
        self.myTemplateRect.templateRectPosChangedSignal.connect(self.updateRectPos)

    def initUi(self):
        from .ccdTemplateBase import TemplateImage
        from .ccdview import ccdImageView
        aoiRect = ccdImageView.GetAoi() # 获取图像尺寸
        self.imageRect = QRect(2, 2, aoiRect.width, aoiRect.height)
        self.dialogRect = QRect(0, 0, self.imageRect.width()+120, self.imageRect.height()+55) # 窗口尺寸

        self.myTemplateImage = TemplateImage(self) # 模板图像尺寸
        self.myTemplateImage.setGeometry(self.imageRect)

        self.myTemplateRect = TemplateRect(self)
        self.myTemplateRect.setGeometry(self.imageRect)
        self.myTemplateRect.templateRect.setRect((self.modelData.ptPosError.x - self.modelData.nTrackerWidth/ 2),
                                                 (self.modelData.ptPosError.y - self.modelData.nTrackerHeight/ 2),
                                                  self.modelData.nTrackerWidth,
                                                  self.modelData.nTrackerHeight)


        infoText = "按住方向键,以移动识别框; 同时按住Ctrl+方向键,快速移动识别框;\n输入坐标值可设定识别框位置"
        self.infoLabel = QLabel(infoText, self)
        self.infoLabel.setGeometry(5, self.imageRect.height()+5, self.imageRect.width(), 50)

        self.xLabel = QLabel("center X:", self)
        self.xLabel.setGeometry(self.imageRect.width() + 10, self.dialogRect.top() + 5, 100, 30)
        self.xPosEdit = PyIntegerLineEdit(self)
        self.xPosEdit.setGeometry(self.imageRect.width() + 10, self.dialogRect.top() + 35, 100, 30)
        self.xPosEdit.editingFinished.connect(self.on_modifyXPos)

        self.yLabel = QLabel("Center Y:", self)
        self.yLabel.setGeometry(self.imageRect.width() + 10, self.dialogRect.top() + 70, 100, 30)
        self.yPosEdit = PyIntegerLineEdit(self)
        self.yPosEdit.setGeometry(self.imageRect.width() + 10, self.dialogRect.top() + 100, 100, 30)
        self.yPosEdit.editingFinished.connect(self.on_modifyYPos)

        self.grabAgainBtn = QPushButton("GrabAgain", self)
        self.grabAgainBtn.setGeometry(self.imageRect.width()+10, self.dialogRect.bottom()-135, 100, 30)
        self.OKBtn = QPushButton("OK", self)
        self.OKBtn.setGeometry(self.imageRect.width()+10, self.dialogRect.bottom()-90, 100, 30)
        self.CancelBtn = QPushButton("Cancel", self)
        self.CancelBtn.setGeometry(self.imageRect.width()+10, self.dialogRect.bottom()-45, 100, 30)

        self.setGeometry(self.dialogRect)

    def updateRectPos(self):
        self.xPosEdit.setValue(self.myTemplateRect.templateRect.center().x())
        self.yPosEdit.setValue(self.myTemplateRect.templateRect.center().y())

    def on_modifyXPos(self):
        xPos = self.xPosEdit.value()
        if xPos in range(0, self.imageRect.width()):
            self.myTemplateRect.templateRect.setRect(xPos-self.myTemplateRect.templateRect.width()/2,
                                                     self.myTemplateRect.templateRect.top(),
                                                     self.myTemplateRect.templateRect.width(),
                                                     self.myTemplateRect.templateRect.height())
            self.myTemplateRect.update()
        else:
            _logger.warning(_translate("findModelAgain", "x pos is out of range."))

    def on_modifyYPos(self):
        yPos = self.yPosEdit.value()
        if yPos in range(0, self.imageRect.height()):
            self.myTemplateRect.templateRect.setRect(self.myTemplateRect.templateRect.left(),
                                                     yPos-self.myTemplateRect.templateRect.height()/2,
                                                     self.myTemplateRect.templateRect.width(),
                                                     self.myTemplateRect.templateRect.height())
            self.myTemplateRect.update()
        else:
            _logger.warning(_translate("findModelAgain", "y pos is out of range."))

    def on_grabAgain(self):
        self.myTemplateImage.repaint()

    def on_OK(self):
        self.modelData.ptPosError.x = self.myTemplateRect.templateRect.center().x()
        self.modelData.ptPosError.y = self.myTemplateRect.templateRect.center().y()
        self.close()

    def on_Cancel(self):
        self.close()

    def done(self, result):
        super(AssistRecognizeDlg, self).done(result)
        AssistRecognizeDlg.instance_count -= 1


def showAssistRecognizeDlg(modelData):
    if AssistRecognizeDlg.instance_count < 1:
        assistRecognizeDlg = AssistRecognizeDlg(modelData)
        geometry = assistRecognizeDlg.geometry()
        geometry.moveCenter(basic.mainWindow.geometry().center())
        assistRecognizeDlg.setGeometry(geometry)
        assistRecognizeDlg.exec_()
        assistRecognizeDlg.destroy()


class FindModelAgainDlg(QDialog):

    showFindModelAgainDlgSignal = QtCore.pyqtSignal(QtCore.QVariant)

    def __init__(self, parent=None):
        super(FindModelAgainDlg, self).__init__(parent)
        self.ui = basic.loadUi(self, ":/common/ccd/findModelAgainDlg.ui")
        self.ui.tryAgainBtn.clicked.connect(self.on_tryAgain)
        self.ui.skipBtn.clicked.connect(self.on_skip)
        self.ui.quitBtn.clicked.connect(self.on_quit)
        self.ui.assistRecognizeBtn.clicked.connect(self.on_assistRecognize)
        self.showFindModelAgainDlgSignal.connect(self.showDlg, QtCore.Qt.BlockingQueuedConnection)

    def updateUi(self, data):
        self.modelData = data
        if not self.modelData.bCanIgnore:
            self.ui.skipBtn.setEnabled(False)
        else:
            self.ui.skipBtn.setEnabled(True)
        if self.modelData.bNotRecognized:
            self.setWindowTitle("第{}次-识别失败".format(self.modelData.nFailCount))
            self.ui.infoLabel.setText("识别度")
            self.ui.resolutionEdit.setText("{:.3f}".format(self.modelData.nScore))
        else:
            self.setWindowTitle("第{}次-位置误差过大".format(self.modelData.nFailCount))
            self.ui.infoLabel.setText("位置差")
            self.ui.resolutionEdit.setText("({:.3f}, {:.3f})".format(
                self.modelData.ptPosError.x, self.modelData.ptPosError.y))
        self.ui.panelEdit.setText("{}".format(self.modelData.nPanelNo))
        self.ui.singlePieceEdit.setText("{}".format(self.modelData.nPieceNo))
        self.ui.grabPointEdit.setText("{}".format(self.modelData.nGrabNo))
        self.ui.thresholdEdit.setValue(self.modelData.nThreshold)

    def on_tryAgain(self):
        self.modelData.nThreshold = self.ui.thresholdEdit.value()
        self.modelData.nRet = _cnc.FIND_AGAIN_RETRY
        self.close()

    def on_skip(self):
        self.modelData.nRet = _cnc.FIND_AGAIN_IGNORE
        self.close()

    def on_quit(self):
        self.modelData.nRet = _cnc.FIND_AGAIN_EXIT
        self.close()

    def on_assistRecognize(self):
        self.modelData.nRet = _cnc.FIND_AGAIN_MANUAL_FIND
        showAssistRecognizeDlg(self.modelData)

    def showDlg(self, data):
        geometry = self.geometry()
        geometry.moveCenter(basic.mainWindow.geometry().center())
        self.setGeometry(geometry)
        self.updateUi(data)
        self.exec_()
        self.destroy()


findModelAgainDlg = FindModelAgainDlg(basic.mainWindow)


#multipanelprocessdlg.py

import logging
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from .ccdview import ccdImageView
import basic
import _cnc

_logger = logging.getLogger(__name__)
_translate = QtCore.QCoreApplication.translate

class MultiPanelProcessDlg(QDialog):

    def __init__(self, parent=None):
        super(MultiPanelProcessDlg, self).__init__(parent)
        self.ui = basic.loadUi(self, ":/common/ccd/multipanelprocessdlg.ui")
        self.multiPanelModify = _cnc.CCcdSettingsDlg()
        self.ccdMultiPanel = ccdImageView.GetCcdPanel()
        self.ccdMultiPanelPropertyDict = {}
        self.maxRowCount = self.ccdMultiPanel.GetPanelCountMax()
        for row_index in range(self.maxRowCount):
            self.ui.panelTableWidget.setItem(row_index, 0, QTableWidgetItem("0.000"))
            self.ui.panelTableWidget.setItem(row_index, 1, QTableWidgetItem("0.000"))
        self.updateUi()
        self.ui.panelTableWidget.itemChanged.connect(self.on_setOffset)
        self.ui.panelCountEdit.editingFinished2.connect(self.on_setPanelCount)
        self.ui.startIndexEdit.editingFinished2.connect(self.on_setStartIndex)
        self.ui.useLessToolsCheckbox.stateChanged.connect(self.on_useLessTools)
        self.ui.twoPanelCycleCheckbox.stateChanged.connect(self.on_twoPanelCycle)
        self.ui.clearAllBtn.clicked.connect(self.on_clearAll)
        self.ui.OKBtn.clicked.connect(self.on_OK)
        self.ui.CancelBtn.clicked.connect(self.on_Cancel)

    def getCcdMultiPanelProperty(self):
        self.ccdMultiPanelPropertyDict["panelCount"] = self.ccdMultiPanel.nPanelCount
        self.ccdMultiPanelPropertyDict["panelStart"] = self.ccdMultiPanel.nPanelStart
        self.ccdMultiPanelPropertyDict["leastToolChange"] = self.ccdMultiPanel.bLeastToolChange
        self.ccdMultiPanelPropertyDict["cycleMachining"] = self.ccdMultiPanel.bCycleMachining

    def setCcdMultiPanelProperty(self):
        self.ccdMultiPanel.nPanelCount = self.ccdMultiPanelPropertyDict["panelCount"]
        self.ccdMultiPanel.nPanelStart = self.ccdMultiPanelPropertyDict["panelStart"]
        self.ccdMultiPanel.bLeastToolChange = self.ccdMultiPanelPropertyDict["leastToolChange"]
        self.ccdMultiPanel.bCycleMachining = self.ccdMultiPanelPropertyDict["cycleMachining"]

    def updateUi(self):
        self.getCcdMultiPanelProperty()
        self.ui.panelCountEdit.setValue(self.ccdMultiPanelPropertyDict["panelCount"])
        self.ui.startIndexEdit.setValue(self.ccdMultiPanelPropertyDict["panelStart"])
        self.ui.twoPanelCycleCheckbox.setChecked(self.ccdMultiPanelPropertyDict["cycleMachining"])
        self.ui.useLessToolsCheckbox.setChecked(self.ccdMultiPanelPropertyDict["leastToolChange"])
        for panel_index in range(self.ccdMultiPanel.nPanelCount):
            self.getOffset(panel_index)

    def getOffset(self, row_index):
        xOffset = self.ccdMultiPanel.GetPanelOffset(row_index).x
        yOffset = self.ccdMultiPanel.GetPanelOffset(row_index).y
        xOffsetItem = QTableWidgetItem("{:.3f}".format(xOffset))
        yOffsetItem = QTableWidgetItem("{:.3f}".format(yOffset))
        self.ui.panelTableWidget.setItem(row_index, 0, xOffsetItem)
        self.ui.panelTableWidget.setItem(row_index, 1, yOffsetItem)

    def on_setOffset(self, item):
        rowIndex = self.ui.panelTableWidget.row(item)
        if self.ui.panelTableWidget.item(rowIndex, 0) and self.ui.panelTableWidget.item(rowIndex, 0).text():
            xOffset = float(self.ui.panelTableWidget.item(rowIndex, 0).text())
        else:
            _logger.warning(_translate("multipanelprocessdlg", "Invalid value"))
            return
        if self.ui.panelTableWidget.item(rowIndex, 1) and self.ui.panelTableWidget.item(rowIndex, 1).text():
            yOffset = float(self.ui.panelTableWidget.item(rowIndex, 1).text())
        else:
            _logger.warning(_translate("multipanelprocessdlg", "Invalid value"))
            return
        self.ccdMultiPanel.SetPanelOffset(rowIndex, _cnc.CMvRealPoint(xOffset, yOffset, 0))
        self.multiPanelModify.SetCcdParamChanged(_cnc.CCD_PARAM_PANEL)

    def on_setPanelCount(self):
        panelCount = self.ui.panelCountEdit.value()
        if panelCount <= self.maxRowCount:
            self.ccdMultiPanelPropertyDict["panelCount"] = self.ui.panelCountEdit.value()
        else:
            self.ui.panelCountEdit.setValue(self.ui.panelCountEdit.lastValue)
            _logger.warning(_translate("multipanelprocessdlg", "Panel count must lower than 100."))

    def on_setStartIndex(self):
        panelCount = self.ui.panelCountEdit.value()
        startIndex = self.ui.startIndexEdit.value()
        if startIndex <= panelCount:
            self.ccdMultiPanelPropertyDict["panelStart"] = self.ui.startIndexEdit.value()
        else:
            self.ui.panelCountEdit.setValue(self.ui.panelCountEdit.lastValue)
            _logger.warning(_translate("multipanelprocessdlg", "Panel start number must lower than panel count."))

    def on_useLessTools(self, status):
        if status:
            self.ccdMultiPanelPropertyDict["leastToolChange"] = True
        else:
            self.ccdMultiPanelPropertyDict["leastToolChange"] = False

    def on_twoPanelCycle(self, status):
        if status:
            self.ccdMultiPanelPropertyDict["cycleMachining"] = True
        else:
            self.ccdMultiPanelPropertyDict["cycleMachining"] = False

    def on_clearAll(self):
        for row_index in range(self.ccdMultiPanel.nPanelCount):
            xOffsetItem = QTableWidgetItem("0.000")
            yOffsetItem = QTableWidgetItem("0.000")
            self.ui.panelTableWidget.setItem(row_index, 0, xOffsetItem)
            self.ui.panelTableWidget.setItem(row_index, 1, yOffsetItem)

    def on_OK(self):
        self.setCcdMultiPanelProperty()
        self.multiPanelModify.SetCcdParamChanged(_cnc.CCD_PARAM_PANEL)
        self.close()

    def on_Cancel(self):
        self.close()


def showMultiPanelProcessDlg():
    basic.showWindow(MultiPanelProcessDlg)

# multipathlayoutdlg.py
# 
import logging, os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QFileDialog
from . import ccdmaskdlg
from .ccdview import ccdImageView
import basic
import _cnc

_logger = logging.getLogger(__name__)
_translate = QtCore.QCoreApplication.translate

class MultiPathLayoutDlg(QDialog):

    def __init__(self, parent=None):
        super(MultiPathLayoutDlg, self).__init__(parent)
        self.ui = basic.loadUi(self, ":/common/ccd/multipathlayoutdlg.ui")
        self.multiPathModify = _cnc.CCcdSettingsDlg()
        self.multiPathList = [{}, {}, {}, {}, {}, {}]
        self.currentPath = 0
        self.ccdSetting = ccdImageView.GetCcdSetting(self.currentPath)
        self.ccdOption = ccdImageView.GetCcdOption()
        for item in ["Path1", "Path2", "Path3", "Path4", "Path5", "Path6"]:
            self.ui.pathListWidget.addItem(item)
        self.ui.pathListWidget.setCurrentRow(self.currentPath)
        self.updateUi(self.currentPath)
        self.ui.pathListWidget.currentRowChanged.connect(self.on_selectPath)
        self.ui.validCheckBox.stateChanged.connect(self.on_setPathValid)
        self.ui.setTemplateBtn.clicked.connect(self.on_settingTemplate)
        self.ui.CCDOriginBtn.clicked.connect(self.on_settingOrigin)
        self.ui.pieceCountX.editingFinished2.connect(self.on_setProductArray)
        self.ui.pieceCountY.editingFinished2.connect(self.on_setProductArray)
        self.ui.pieceOffsetX.editingFinished2.connect(self.on_setProductArray)
        self.ui.pieceOffsetY.editingFinished2.connect(self.on_setProductArray)
        self.ui.outputFilePath.editingFinished.connect(self.on_setOutputFile)
        self.ui.inputPathBtn.clicked.connect(self.on_openInputFile)
        self.ui.outputPathBtn.clicked.connect(self.on_saveOutputFile)
        self.ui.ignoreSkewPtCheckbox.stateChanged.connect(self.on_ignoreSkewPt)
        self.ui.convertBtn.clicked.connect(self.on_convert)
        self.ui.ApplyBtn.clicked.connect(self.on_Apply)
        self.ui.CancelBtn.clicked.connect(self.on_Cancel)

    def on_selectPath(self, path_index):
        _logger.debug("current path = {}".format(self.currentPath))
        self.applyLastChanges()
        self.currentPath = path_index
        self.ccdSetting = ccdImageView.GetCcdSetting(self.currentPath)
        self.updateUi(self.currentPath)

    def updateUi(self, path_index):
        self.getPathProperty(path_index)
        self.ui.pathNameLable.setText("Path{}".format(path_index + 1))
        self.ui.validCheckBox.setChecked(self.multiPathList[path_index]["valid"])
        self.ui.pieceCountX.setValue(self.multiPathList[path_index]["pieceCountX"])
        self.ui.pieceCountY.setValue(self.multiPathList[path_index]["pieceCountY"])
        self.ui.pieceOffsetX.setValue(self.multiPathList[path_index]["pieceOffsetX"])
        self.ui.pieceOffsetY.setValue(self.multiPathList[path_index]["pieceOffsetY"])
        self.ui.inputFilePath.setText(self.multiPathList[path_index]["inputFile"])
        self.ui.outputFilePath.setText(self.multiPathList[path_index]["outputFile"])
        if path_index > 0:
            self.ui.outputFilePath.setEnabled(False)
            self.ui.outputFilePath.setVisible(False)
            self.ui.outputPathBtn.setEnabled(False)
            self.ui.outputPathBtn.setVisible(False)
            self.ui.outputFileLabel.setVisible(False)
        else:
            self.ui.outputFilePath.setEnabled(True)
            self.ui.outputFilePath.setVisible(True)
            self.ui.outputPathBtn.setEnabled(True)
            self.ui.outputPathBtn.setVisible(True)
            self.ui.outputFileLabel.setVisible(True)
        self.ui.ignoreSkewPtCheckbox.setChecked(self.multiPathList[path_index]["ignoreSkewPt"])
        if not self.multiPathList[path_index]["valid"]:
            self.setPathValid(False)
        else:
            self.setPathValid(True)

    def getPathProperty(self, path_index):
        self.multiPathList[path_index]["valid"] = self.ccdSetting.bValid
        self.multiPathList[path_index]["pieceCountX"] = self.ccdSetting.nPieceCountX
        self.multiPathList[path_index]["pieceCountY"] = self.ccdSetting.nPieceCountY
        self.multiPathList[path_index]["pieceOffsetX"] = self.ccdSetting.nPieceOffsetX
        self.multiPathList[path_index]["pieceOffsetY"] = self.ccdSetting.nPieceOffsetY
        self.multiPathList[path_index]["inputFile"] = self.ccdSetting.GetInFilePath()
        self.multiPathList[path_index]["outputFile"] = self.ccdSetting.GetOutFilePath()
        self.multiPathList[path_index]["ignoreSkewPt"] = self.ccdOption.bIgnoreSkewPoint

    def setPathProperty(self, path_index):
        self.ccdSetting.bValid = self.multiPathList[path_index]["valid"]
        self.ccdSetting.nPieceCountX = self.multiPathList[path_index]["pieceCountX"]
        self.ccdSetting.nPieceCountY = self.multiPathList[path_index]["pieceCountY"]
        self.ccdSetting.nPieceOffsetX = self.multiPathList[path_index]["pieceOffsetX"]
        self.ccdSetting.nPieceOffsetY = self.multiPathList[path_index]["pieceOffsetY"]
        self.ccdSetting.SetInFilePath(self.multiPathList[path_index]["inputFile"])
        self.ccdSetting.SetOutFilePath(self.multiPathList[path_index]["outputFile"])
        self.ccdOption.bIgnoreSkewPoint = self.multiPathList[path_index]["ignoreSkewPt"]

    def setPathValid(self, valid):
        for widget in [self.ui.setTemplateBtn, self.ui.CCDOriginBtn, self.ui.layoutGroupBox,
                       self.ui.inoutputGroupBox, self.ui.convertBtn, self.ui.ApplyBtn, self.ui.CancelBtn]:
            widget.setEnabled(valid)

    def on_setPathValid(self, status):
        if status:
            self.multiPathList[self.currentPath]["valid"] = True
        else:
            self.multiPathList[self.currentPath]["valid"] = False
        self.setPathValid(self.multiPathList[self.currentPath]["valid"])
        if self.currentPath > 0:
            self.ui.outputFilePath.setEnabled(False)
            self.ui.outputFilePath.setVisible(False)
            self.ui.outputPathBtn.setEnabled(False)
            self.ui.outputPathBtn.setVisible(False)
            self.ui.outputFileLabel.setVisible(False)
        else:
            self.ui.outputFilePath.setEnabled(True)
            self.ui.outputFilePath.setVisible(True)
            self.ui.outputPathBtn.setEnabled(True)
            self.ui.outputPathBtn.setVisible(True)
            self.ui.outputFileLabel.setVisible(True)

    def on_settingTemplate(self):
        ccdmaskdlg.showCCDMaskDlg(self.currentPath, self)

    def on_settingOrigin(self):
        from .ccdoriginposdlg import showCCDOriginPosDlg
        showCCDOriginPosDlg(self.currentPath, self)

    def on_setProductArray(self):
        if self.sender() == self.ui.pieceCountX:
            self.multiPathList[self.currentPath]["pieceCountX"] = self.ui.pieceCountX.value()
        elif self.sender() == self.ui.pieceCountY:
            self.multiPathList[self.currentPath]["pieceCountY"] = self.ui.pieceCountY.value()
        elif self.sender() == self.ui.pieceOffsetX:
            self.multiPathList[self.currentPath]["pieceOffsetX"] = self.ui.pieceOffsetX.value()
        elif self.sender() == self.ui.pieceOffsetY:
            self.multiPathList[self.currentPath]["pieceOffsetY"] = self.ui.pieceOffsetY.value()

    def on_openInputFile(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, "选择NC文件", basic.ncDir, "Select Files (*.nc)")
        if fileName:
            self.ui.inputFilePath.setText(os.path.realpath(fileName))
            outputFileName = "{}.ccd".format(os.path.splitext(os.path.basename(fileName))[0])
            outputFile = os.path.join(os.path.dirname(fileName), outputFileName)
            self.ui.outputFilePath.setText(os.path.realpath(outputFile))
            self.multiPathList[self.currentPath]["inputFile"] = os.path.realpath(fileName)
            self.multiPathList[self.currentPath]["outputFile"] = os.path.realpath(outputFile)

    def on_saveOutputFile(self):
        fileDir = QFileDialog.getExistingDirectory(self, "选择文件路径", basic.ncDir)
        if fileDir:
            outputFileName = self.ui.outputFilePath.text()
            if outputFileName:
                outputFile = os.path.join(fileDir, os.path.basename(outputFileName))
                outputFile = os.path.realpath(outputFile)
                self.ui.outputFilePath.setText(outputFile)
                self.multiPathList[self.currentPath]["outputFile"] = outputFile

    def on_setOutputFile(self):
        outputFilePath = self.ui.outputFilePath.text()
        if outputFilePath:
            if os.path.exists(os.path.dirname(outputFilePath)):
                self.multiPathList[self.currentPath]["outputFile"] = outputFilePath
            else:
                _logger.error(_translate("multipathlayoutdlg", "Output file path is not exist."))
                self.ui.outputFilePath.setText(self.multiPathList[self.currentPath]["outputFile"])
        else:
            _logger.warning(_translate("multipathlayoutdlg", "Output file path can not be empty, please try again."))
            self.ui.outputFilePath.setText(self.multiPathList[self.currentPath]["outputFile"])

    def on_ignoreSkewPt(self, status):
        if status:
            self.multiPathList[self.currentPath]["ignoreSkewPt"] = True
        else:
            self.multiPathList[self.currentPath]["ignoreSkewPt"] = False

    def on_convert(self):
        result =  ccdImageView.ConvertFile(True)
        _logger.info(_translate("multipathlayoutdlg", "convert result: {}").format(_cnc.GetErrString(result)))

    def applyLastChanges(self):
        if self.multiPathList[self.currentPath]:
            self.setPathProperty(self.currentPath)
            self.multiPathModify.SetCcdParamChanged(_cnc.CCD_PARAM_SETTING)
            self.multiPathModify.SetCcdParamChanged(_cnc.CCD_PARAM_OPTION)

    def on_Apply(self):
        self.applyLastChanges()

    def on_Cancel(self):
        self.close()


multiPathLayoutDlg = MultiPathLayoutDlg(basic.mainWindow)

def showMultiPathLayoutDlg():
    if multiPathLayoutDlg.isVisible():
        multiPathLayoutDlg.raise_()
        multiPathLayoutDlg.activateWindow()
    else:
        geometry = multiPathLayoutDlg.geometry()
        geometry.moveCenter(basic.mainWindow.geometry().center())
        multiPathLayoutDlg.setGeometry(geometry)
        multiPathLayoutDlg.show()
    multiPathLayoutDlg.updateUi(multiPathLayoutDlg.currentPath)    



# productarraydlg.py
# 
import os, logging
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog
from .ccdview import ccdImageView
import basic
import _cnc

_logger = logging.getLogger(__name__)
_translate = QtCore.QCoreApplication.translate

class ProductArrayDlg(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(ProductArrayDlg, self).__init__(parent)
        self.ui = basic.loadUi(self, ":/common/ccd/productarraydlg.ui")
        self.productArrayModify = _cnc.CCcdSettingsDlg()
        self.ccdOption = ccdImageView.GetCcdOption()
        self.ccdSetting = ccdImageView.GetCcdSetting(0)
        self.productArrayProperty = {}
        self.updateUi()
        self.ui.pieceCountX.editingFinished2.connect(self.on_setProductArray)
        self.ui.pieceCountY.editingFinished2.connect(self.on_setProductArray)
        self.ui.pieceOffsetX.editingFinished2.connect(self.on_setProductArray)
        self.ui.pieceOffsetY.editingFinished2.connect(self.on_setProductArray)
        self.ui.outputFilePath.editingFinished.connect(self.on_setOutputFile)
        self.ui.inputPathBtn.clicked.connect(self.on_openInputFile)
        self.ui.outputPathBtn.clicked.connect(self.on_saveOutputFile)
        self.ui.convertBtn.clicked.connect(self.on_convert)
        self.ui.ignoreSkewPtCheckbox.stateChanged.connect(self.on_ignoreSkewPt)
        self.ui.CancelBtn.clicked.connect(self.on_Cancel)
        self.ui.OKBtn.clicked.connect(self.on_OK)

    def getProductArrayProperty(self):
        self.productArrayProperty["pieceCountX"] = self.ccdSetting.nPieceCountX
        self.productArrayProperty["pieceCountY"] = self.ccdSetting.nPieceCountY
        self.productArrayProperty["pieceOffsetX"] = self.ccdSetting.nPieceOffsetX
        self.productArrayProperty["pieceOffsetY"] = self.ccdSetting.nPieceOffsetY
        self.productArrayProperty["inputFile"] = self.ccdSetting.GetInFilePath()
        self.productArrayProperty["outputFile"] = self.ccdSetting.GetOutFilePath()
        self.productArrayProperty["ignoreSkewPt"] = self.ccdOption.bIgnoreSkewPoint

    def setProductArrayProperty(self):
        self.ccdSetting.nPieceCountX = self.productArrayProperty["pieceCountX"]
        self.ccdSetting.nPieceCountY = self.productArrayProperty["pieceCountY"]
        self.ccdSetting.nPieceOffsetX = self.productArrayProperty["pieceOffsetX"]
        self.ccdSetting.nPieceOffsetY = self.productArrayProperty["pieceOffsetY"]
        self.ccdSetting.SetInFilePath(self.productArrayProperty["inputFile"])
        self.ccdSetting.SetOutFilePath(self.productArrayProperty["outputFile"])
        self.ccdOption.bIgnoreSkewPoint = self.productArrayProperty["ignoreSkewPt"]

    def updateUi(self):
        self.getProductArrayProperty()
        self.ui.pieceCountX.setValue(self.productArrayProperty["pieceCountX"])
        self.ui.pieceCountY.setValue(self.productArrayProperty["pieceCountY"])
        self.ui.pieceOffsetX.setValue(self.productArrayProperty["pieceOffsetX"])
        self.ui.pieceOffsetY.setValue(self.productArrayProperty["pieceOffsetY"])
        self.ui.inputFilePath.setText(self.productArrayProperty["inputFile"])
        self.ui.outputFilePath.setText(self.productArrayProperty["outputFile"])
        self.ui.ignoreSkewPtCheckbox.setChecked(self.productArrayProperty["ignoreSkewPt"])

    def on_setProductArray(self):
        if self.sender() == self.ui.pieceCountX:
            self.productArrayProperty["pieceCountX"] = self.ui.pieceCountX.value()
        elif self.sender() == self.ui.pieceCountY:
            self.productArrayProperty["pieceCountY"] = self.ui.pieceCountY.value()
        elif self.sender() == self.ui.pieceOffsetX:
            self.productArrayProperty["pieceOffsetX"] = self.ui.pieceOffsetX.value()
        elif self.sender() == self.ui.pieceOffsetY:
            self.productArrayProperty["pieceOffsetY"] = self.ui.pieceOffsetY.value()

    def on_openInputFile(self):
        fileName, fileType  = QFileDialog.getOpenFileName(self, "选择NC文件", basic.ncDir, "Select Files (*.nc)")
        if fileName:
            self.ui.inputFilePath.setText(os.path.realpath(fileName))
            outputFileName = "{}.ccd".format(os.path.splitext(os.path.basename(fileName))[0])
            outputFile = os.path.join(os.path.dirname(fileName), outputFileName)
            self.ui.outputFilePath.setText(os.path.realpath(outputFile))
            self.productArrayProperty["inputFile"] = os.path.realpath(fileName)
            self.productArrayProperty["outputFile"] = os.path.realpath(outputFile)

    def on_saveOutputFile(self):
        fileDir = QFileDialog.getExistingDirectory(self, "选择文件路径", basic.ncDir)
        if fileDir:
            outputFileName = self.ui.outputFilePath.text()
            if outputFileName:
                outputFile = os.path.join(fileDir, os.path.basename(outputFileName))
                outputFile = os.path.realpath(outputFile)
                self.ui.outputFilePath.setText(outputFile)
                self.productArrayProperty["outputFile"] = outputFile

    def on_setOutputFile(self):
        outputFilePath = self.ui.outputFilePath.text()
        if outputFilePath:
            if os.path.exists(os.path.dirname(outputFilePath)):
                self.productArrayProperty["outputFile"] = outputFilePath
            else:
                _logger.error(_translate("productarraydlg", "Output file path is not exist."))
                self.ui.outputFilePath.setText(self.productArrayProperty["outputFile"])
        else:
            _logger.warning(_translate("productarraydlg", "Output file path can not be empty, please try again."))
            self.ui.outputFilePath.setText(self.productArrayProperty["outputFile"])

    def on_ignoreSkewPt(self, status):
        if status:
            self.productArrayProperty["ignoreSkewPt"] = True
        else:
            self.productArrayProperty["ignoreSkewPt"] = False

    def applyProductArrayProperty(self):
        self.setProductArrayProperty()
        self.productArrayModify.SetCcdParamChanged(_cnc.CCD_PARAM_OPTION)
        self.productArrayModify.SetCcdParamChanged(_cnc.CCD_PARAM_SETTING)

    def on_convert(self):
        self.applyProductArrayProperty()
        result = ccdImageView.ConvertFile()
        _logger.info(_translate("productarraydlg", "convert result: {}").format(_cnc.GetErrString(result)))

    def on_OK(self):
        self.applyProductArrayProperty()
        self.close()

    def on_Cancel(self):
        self.close()


productArrayDlg = ProductArrayDlg(basic.mainWindow)

def showProductArrayDlg():
    if productArrayDlg.isVisible():
        productArrayDlg.raise_()
        productArrayDlg.activateWindow()
    else:
        geometry = productArrayDlg.geometry()
        geometry.moveCenter(basic.mainWindow.geometry().center())
        productArrayDlg.setGeometry(geometry)
        productArrayDlg.show()
    productArrayDlg.updateUi()


# ccdpropertydlg.py
# 
from PyQt5.QtWidgets import QDialog
from .ccdview import ccdImageView
import basic
import _cnc
from basic import R, unit

class CCDPropertyDlg(QDialog):

    def __init__(self, parent=None):
        super(CCDPropertyDlg, self).__init__(parent)
        self.ui = basic.loadUi(self, ":/common/ccd/CCDpropertydlg.ui")
        self.CCDPropertyModify = _cnc.CCcdSettingsDlg()
        self.ccdPropertyDict = {}
        self.ccdProperty = ccdImageView.GetCcdProperty()
        self.updateUi()
        self.ui.xResolutionEdit.editingFinished2.connect(self.on_setXCCDResolution)
        self.ui.yResolutionEdit.editingFinished2.connect(self.on_setYCCDResolution)
        self.ui.xSpanToSpinEdit.editingFinished2.connect(self.on_setXSpanToSpin)
        self.ui.ySpanToSpinEdit.editingFinished2.connect(self.on_setYSpanToSpin)
        self.ui.getSpinXYPosBtn.clicked.connect(self.on_getSpinXYPos)
        self.ui.getCcdXYPosBtn.clicked.connect(self.on_getCcdXYPos)
        self.ui.OKBtn.clicked.connect(self.on_OK)
        self.ui.CancelBtn.clicked.connect(self.on_Cancel)

    def updateUi(self):
        self.getCCDProperty()
        self.ui.xResolutionEdit.setValue(self.ccdPropertyDict.get("CCDResolutionX", -1.0))
        self.ui.yResolutionEdit.setValue(self.ccdPropertyDict.get("CCDResolutionY", -1.0))
        self.ui.xSpanToSpinEdit.setValue(self.ccdPropertyDict.get("CCDToSpindleX", -1))
        self.ui.ySpanToSpinEdit.setValue(self.ccdPropertyDict.get("CCDToSpindleY", -1))

    def getCCDProperty(self):
        self.ccdPropertyDict["CCDResolutionX"] = self.ccdProperty.nCcdResolutionX
        self.ccdPropertyDict["CCDResolutionY"] = self.ccdProperty.nCcdResolutionY
        self.ccdPropertyDict["CCDToSpindleX"] = self.ccdProperty.nCcdToSpindleX
        self.ccdPropertyDict["CCDToSpindleY"] = self.ccdProperty.nCcdToSpindleY

    def setCCDProperty(self):
        self.ccdProperty.nCcdResolutionX = self.ccdPropertyDict["CCDResolutionX"]
        self.ccdProperty.nCcdResolutionY = self.ccdPropertyDict["CCDResolutionY"]
        self.ccdProperty.nCcdToSpindleX = self.ccdPropertyDict["CCDToSpindleX"]
        self.ccdProperty.nCcdToSpindleY = self.ccdPropertyDict["CCDToSpindleY"]

    def on_setXCCDResolution(self):
        self.ccdPropertyDict["CCDResolutionX"] = self.ui.xResolutionEdit.value()

    def on_setYCCDResolution(self):
        self.ccdPropertyDict["CCDResolutionY"] = self.ui.yResolutionEdit.value()

    def on_setXSpanToSpin(self):
        self.ccdPropertyDict["CCDToSpindleX"] = self.ui.xSpanToSpinEdit.value()

    def on_setYSpanToSpin(self):
        self.ccdPropertyDict["CCDToSpindleY"] = self.ui.ySpanToSpinEdit.value()

    def on_getSpinXYPos(self):
        self.spin_x = R[101]*unit.cnc2hmiLength
        self.spin_y = R[102]*unit.cnc2hmiLength
        self.ui.spinPosLabel.setText("({:.3f}, {:.3f})".format(self.spin_x, self.spin_y))

    def on_getCcdXYPos(self):
        self.ccd_x =  R[101]*unit.cnc2hmiLength
        self.ccd_y = R[102]*unit.cnc2hmiLength
        self.ui.ccdPosLabel.setText("({:.3f}, {:.3f})".format(self.ccd_x, self.ccd_y))
        self.ui.xSpanToSpinEdit.setValue(self.ccd_x - self.spin_x)
        self.ccdPropertyDict["CCDToSpindleX"] = self.ui.xSpanToSpinEdit.value()
        self.ui.ySpanToSpinEdit.setValue(self.ccd_y - self.spin_y)
        self.ccdPropertyDict["CCDToSpindleY"] = self.ui.ySpanToSpinEdit.value()


    def on_OK(self):
        if self.ccdPropertyDict:
            self.setCCDProperty()
        self.CCDPropertyModify.SetCcdParamChanged(_cnc.CCD_PARAM_PROPERTY)
        self.close()

    def on_Cancel(self):
        self.close()

def showCCDPropertyDlg():
    basic.showWindow(CCDPropertyDlg)


# ccdoriginposdlg.py
# 
import logging
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import gevent
from .ccdview import ccdImageView
from .ccdtemplatedlg import ccdTemplateDlg
import basic
from basic import R, unit
import _cnc

_logger = logging.getLogger(__name__)
_translate = QtCore.QCoreApplication.translate


class CCDOriginPosDlg(QtWidgets.QDialog):

    instance_count = 0
    def __init__(self, path_no=0, parent=None):
        super(CCDOriginPosDlg, self).__init__(parent)
        self.ui = basic.loadUi(self, ":/common/ccd/CCDoriginposdlg.ui")
        CCDOriginPosDlg.instance_count += 1
        self.ccdOriginPosModify = _cnc.CCcdSettingsDlg()
        self.ccdOriginPos = _cnc.CCcdOriginDlg()
        self.pathNo = path_no
        originPos = self.ccdOriginPos.GetCcdOrigin(self.pathNo)
        self.ui.xOriginPosEdit.setValue(originPos.x)
        self.ui.yOriginPosEdit.setValue(originPos.y)
        self.ui.zFocusEdit.setValue(self.ccdOriginPos.GetCcdFocusHeight())
        self.ui.centerPt2Btn.setEnabled(False)
        self.ui.setIntegerOneXYBtn.clicked.connect(self.on_setIntegerOneXY)
        self.ui.setSingleOneXYBtn.clicked.connect(self.on_setSingleOneXY)
        self.ui.setIntegerOneSingleOneXYBtn.clicked.connect(self.on_setIntegerOneSingleOneXY)
        self.ui.setSingleOneSingleTwoXYBtn.clicked.connect(self.on_setSingleOneSingleTwoXY)
        self.ui.centerPt1Btn.clicked.connect(self.on_centerPt1)
        self.ui.centerPt2Btn.clicked.connect(self.on_centerPt2)
        self.ui.setCurrentXYPosBtn.clicked.connect(self.on_setCurrentXYPos)
        self.ui.currentZHeightBtn.clicked.connect(self.on_setCurrentZHeight)
        self.ui.CancelBtn.clicked.connect(self.on_Cancel)
        self.ui.OKBtn.clicked.connect(self.on_OK)
        ccdTemplateDlg.ccdTemplateDlgSetHomeDoneSignal.connect(self.on_setCCDHome)

    def on_setCCDHome(self):
        originPos = self.ccdOriginPos.GetCcdOrigin(self.pathNo)
        self.ui.xOriginPosEdit.setValue(originPos.x)
        self.ui.yOriginPosEdit.setValue(originPos.y)

    def updateOriginPos(self, originPos):
        self.ui.xOriginPosEdit.setValue(originPos.x)
        self.ui.yOriginPosEdit.setValue(originPos.y)
        # self.ccdOriginPos.SetCcdOrigin(originPos, self.pathNo)

    def checkError(self):
        status = ccdImageView.GetLastError()
        if status != _cnc.CCD_ERR_OK:
            _logger.error(_translate("ccdoriginposdlg", "{}".format(_cnc.GetErrString(status))))
            return True
        else:
            return False

    def on_setIntegerOneXY(self):
        _logger.debug("set Integer XY button was clicked")
        grabP1 = self.ccdOriginPos.GetPosOfPoint(_cnc.GRAB_P1, self.pathNo)
        if self.checkError():
            return
        self.updateOriginPos(grabP1)

    def on_setSingleOneXY(self):
        grabP3 = self.ccdOriginPos.GetPosOfPoint(_cnc.GRAB_P3, self.pathNo)
        if self.checkError():
            return
        self.updateOriginPos(grabP3)

    def on_setIntegerOneSingleOneXY(self):
        grabP1 = self.ccdOriginPos.GetPosOfPoint(_cnc.GRAB_P1, self.pathNo)
        if self.checkError():
            return
        grabP3 = self.ccdOriginPos.GetPosOfPoint(_cnc.GRAB_P3, self.pathNo)
        if self.checkError():
            return
        center = _cnc.CMvRealPoint((grabP1.x + grabP3.x) / 2, (grabP1.y + grabP3.y) / 2, 0.0)
        self.updateOriginPos(center)

    def on_setSingleOneSingleTwoXY(self):
        grabP3 = self.ccdOriginPos.GetPosOfPoint(_cnc.GRAB_P3, self.pathNo)
        if self.checkError():
            return
        grabP4 = self.ccdOriginPos.GetPosOfPoint(_cnc.GRAB_P4, self.pathNo)
        if self.checkError():
            return
        center = _cnc.CMvRealPoint((grabP3.x + grabP4.x) / 2, (grabP3.y + grabP4.y) / 2, 0.0)
        self.updateOriginPos(center)

    def on_centerPt1(self):
        def inner():
            from .ccdtemplatedlg import ccdTemplateDlg
            basic.showCCDTemplateDlg()
            while ccdTemplateDlg.isVisible():
                gevent.sleep(0.01)
            self.centerPt1 = []
            self.centerPt1.append(ccdTemplateDlg.templateProperty["templateRefPos"].x)
            self.centerPt1.append(ccdTemplateDlg.templateProperty["templateRefPos"].y)
            self.ui.centerPt2Btn.setEnabled(True)
        gevent.spawn(inner)

    def on_centerPt2(self):
        def inner():
            from .ccdtemplatedlg import ccdTemplateDlg
            basic.showCCDTemplateDlg()
            while ccdTemplateDlg.isVisible():
                gevent.sleep(0.01)
            self.centerPt2 = []
            self.centerPt2.append(ccdTemplateDlg.templateProperty["templateRefPos"].x)
            self.centerPt2.append(ccdTemplateDlg.templateProperty["templateRefPos"].y)
            center = _cnc.CMvRealPoint((self.centerPt1[0] + self.centerPt2[0]) / 2,
                                       (self.centerPt1[1] + self.centerPt2[1]) / 2, 0.0)
            self.updateOriginPos(center)
        gevent.spawn(inner)

    def on_setCurrentXYPos(self):
        currentPt = _cnc.CMvRealPoint(R[101] * unit.cnc2hmiLength,
                                      R[102] * unit.cnc2hmiLength,
                                      R[103] * unit.cnc2hmiLength)
        self.updateOriginPos(currentPt)

    def on_setCurrentZHeight(self):
        zFocus = R[103] * unit.cnc2hmiLength
        self.ccdOriginPos.SetCcdFocusHeight(zFocus)
        self.ui.zFocusEdit.setValue(self.ccdOriginPos.GetCcdFocusHeight())

    def on_OK(self):
        xOriginPos = self.ui.xOriginPosEdit.value()
        yOriginPos = self.ui.yOriginPosEdit.value()
        originPos = _cnc.CMvRealPoint(xOriginPos, yOriginPos, 0.0)
        self.ccdOriginPos.SetCcdOrigin(originPos, self.pathNo)
        self.ccdOriginPos.SetCcdFocusHeight(self.ui.zFocusEdit.value())
        self.close()

    def on_Cancel(self):
        self.close()

    def done(self, result):
        super(CCDOriginPosDlg, self).done(result)
        CCDOriginPosDlg.instance_count -= 1

def showCCDOriginPosDlg(path_no=0, parent=basic.mainWindow):
    if CCDOriginPosDlg.instance_count < 1:
        dlg = CCDOriginPosDlg(path_no, parent)
        dlg.setGeometry(basic.mainWindow.x() + basic.mainWindow.width()/2 - dlg.width()/2,
                        basic.mainWindow.y() + basic.mainWindow.height()/2 - dlg.height()/2,
                        dlg.width(),
                        dlg.height())
        dlg.show()


# ccdoptiondlg.py
# 

import logging
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QFileDialog

from .ccdview import ccdImageView
import basic
import _cnc

_logger = logging.getLogger(__name__)
_translate = QtCore.QCoreApplication.translate


class CCDOptionDlg(QDialog):

    def __init__(self, parent=None):
        super(CCDOptionDlg, self).__init__(parent)
        self.ui = basic.loadUi(self, ":/common/ccd/CCDoptiondlg.ui")
        self.optionModify = _cnc.CCcdSettingsDlg()
        self.ccdOption = ccdImageView.GetCcdOption()
        self.ccdSetting = ccdImageView.GetCcdSetting(0) # option 2的页面设置对应的是path1的页面
        self.ccdOptionProperty = {}
        self.getCCDOptionProperty()
        self.initOptionTab1()
        self.initOptionTab2()
        self.initOptionTab3()
        self.ui.optionTab.setCurrentIndex(0)
        self.ui.OKBtn.clicked.connect(self.on_OK)
        self.ui.CancelBtn.clicked.connect(self.on_Cancel)
        self.ui.ApplyBtn.clicked.connect(self.on_Apply)

    def initOptionTab1(self):
        self.ui.ignoreCCDCheckbox.setChecked(self.ccdOptionProperty["ignoreCCD"])
        self.ui.ignoreSkewPointCheckbox.setChecked(self.ccdOptionProperty["ignoreSkewPt"])
        self.ui.ignoreLocPointCheckbox.setChecked(self.ccdOptionProperty["ignoreLocPoint"])
        self.ui.ignoreFailedCheckbox.setChecked(self.ccdOptionProperty["ignoreFailed"])
        self.ui.manualAssistRecognizeCheckbox.setChecked(self.ccdOptionProperty["manualAssistRecognize"])
        self.ui.ccdGainEdit.setValue(self.ccdOptionProperty["gain"])
        self.ui.ccdExposureTimeEdit.setValue(self.ccdOptionProperty["exposureTime"])
        self.ui.drawCrossCheckbox.setChecked(self.ccdOptionProperty["drawCross"])
        self.ui.drawFrameCircleCheckbox.setChecked(self.ccdOptionProperty["drawFrameCircle"])
        self.ui.drawROICheckbox.setChecked(self.ccdOptionProperty["drawRoi"])
        self.ui.defaultThresholdEdit.setValue(self.ccdOptionProperty["defaultThreshold"])
        self.ui.maxAllowedErrorEdit.setValue(self.ccdOptionProperty["defaultOffsetMax"])
        self.ui.maxAllowedAngleErrorEdit.setValue(self.ccdOptionProperty["defaultAngleMax"])
        self.ui.cameraSettingBtn.clicked.connect(self.on_cameraSetting)
        self.ui.cameraSettingBtn.setEnabled(False)
        self.ui.ignoreCCDCheckbox.stateChanged.connect(self.on_ignoreCCD)
        self.ui.ignoreSkewPointCheckbox.stateChanged.connect(self.on_ignoreSkewPoint)
        self.ui.ignoreLocPointCheckbox.stateChanged.connect(self.on_ignoreLocPoint)
        self.ui.ignoreFailedCheckbox.stateChanged.connect(self.on_ignoreFailed)
        self.ui.manualAssistRecognizeCheckbox.stateChanged.connect(self.on_manualAssistRecognize)
        self.ui.ccdGainEdit.editingFinished2.connect(self.on_setCCDGain)
        self.ui.ccdExposureTimeEdit.editingFinished2.connect(self.on_setCCDExposureTime)
        self.ui.drawCrossCheckbox.stateChanged.connect(self.on_drawCross)
        self.ui.drawFrameCircleCheckbox.stateChanged.connect(self.on_drawFrameCircle)
        self.ui.drawROICheckbox.stateChanged.connect(self.on_drawROI)
        self.ui.defaultThresholdEdit.editingFinished2.connect(self.on_setDefaultThreshold)
        self.ui.maxAllowedErrorEdit.editingFinished2.connect(self.on_setDefaultOffsetMax)
        self.ui.maxAllowedAngleErrorEdit.editingFinished2.connect(self.on_setDefaultAngleMax)

    def initOptionTab2(self):
        self.ui.skewSinglePieceCheckbox.setChecked(self.ccdOptionProperty["skewSinglePiece"])
        self.ui.useLocPoint2Checkbox.setChecked(self.ccdOptionProperty["useLocPoint2"])
        if self.ccdOptionProperty["useLocPoint2"]:
            self.ui.fourPointsRectCheckbox.setEnabled(True)
        else:
            self.ui.fourPointsRectCheckbox.setEnabled(False)
        self.ui.fourPointsRectCheckbox.setChecked(self.ccdOptionProperty["use4PtRect"])
        self.ui.machineUseNcFileCheckbox.setChecked(self.ccdOptionProperty["machiningUseNcFile"])
        self.ui.skewPointCompensationCheckbox.setChecked(self.ccdOptionProperty["compSkewPoint"])
        if int(self.ccdOptionProperty["skewPointsAngle"]) == 0:
            self.ui.skewPointsAngleEdit.setEnabled(False)
            self.ui.horizentalRadioBtn.setChecked(True)
        elif int(self.ccdOptionProperty["skewPointsAngle"]) == 90:
            self.ui.verticalRadioBtn.setChecked(True)
            self.ui.skewPointsAngleEdit.setEnabled(False)
        else:
            self.ui.angleRadioBtn.setChecked(True)
            self.ui.skewPointsAngleEdit.setEnabled(True)
            self.ui.skewPointsAngleEdit.setValue(self.ccdOptionProperty["skewPointsAngle"])
        self.ui.skewSinglePieceCheckbox.stateChanged.connect(self.on_skewSinglePiece)
        self.ui.useLocPoint2Checkbox.stateChanged.connect(self.on_useLocPoint2)
        self.ui.fourPointsRectCheckbox.stateChanged.connect(self.on_fourPointsRect)
        self.ui.machineUseNcFileCheckbox.stateChanged.connect(self.on_machineUseNcFile)
        self.ui.skewPointCompensationCheckbox.stateChanged.connect(self.on_skewPointCompensation)
        self.ui.skewPointsAngleEdit.editingFinished2.connect(self.on_setSkewPointsAngle)
        for radioBtn in [self.ui.horizentalRadioBtn, self.ui.verticalRadioBtn, self.ui.angleRadioBtn]:
            radioBtn.clicked.connect(self.on_selectSkewPointAngle)

    def initOptionTab3(self):
        self.ui.flip180Checkbox.setChecked(self.ccdOptionProperty["flip180"])
        self.ui.waitToBeInPosCheckbox.setChecked(self.ccdOptionProperty["waitToBeInPos"])
        self.ui.inPosErrMaxEdit.setValue(self.ccdOptionProperty["inPosErrMax"])
        self.ui.timeWaitToGrabEdit.setValue(self.ccdOptionProperty["timeWaitToGrab"])
        self.ui.openDoorDelayEdit.setValue(self.ccdOptionProperty["openDoorDelay"])
        self.ui.closeDoorDelayEdit.setValue(self.ccdOptionProperty["closeDoorDelay"])
        self.ui.grabTimeoutEdit.setValue(self.ccdOptionProperty["grabTimeout"])
        for item in ["Basler", "PtGrey", "GFocus", "UNKNOWN"]:
            self.ui.deviceTypeCombox.addItem(item)
        self.ui.deviceTypeCombox.setCurrentIndex(self.ccdOptionProperty["grabberType"])
        if self.ccdOptionProperty["modelFindAlgorithm"] == 0:
            self.ui.modRadioBtn.setChecked(True)
        else:
            self.ui.patRadioBtn.setChecked(True)
        self.ui.subPixelcheckBox.setChecked(self.ccdOptionProperty["subPixel"])
        self.ui.ccdFieldXEdit.setValue(self.ccdOptionProperty["CCDFieldX"] \
                                           if self.ccdOptionProperty["CCDFieldX"] < ccdImageView.GetAoiMax().width \
                                           else ccdImageView.GetAoiMax().width)
        self.ui.ccdFieldYEdit.setValue(self.ccdOptionProperty["CCDFieldY"] \
                                           if self.ccdOptionProperty["CCDFieldY"] < ccdImageView.GetAoiMax().height \
                                           else ccdImageView.GetAoiMax().height)
        self.ui.AOI_XRangeLabel.setText("(1 - {})".format(ccdImageView.GetAoiMax().width))
        self.ui.AOI_YRangeLabel.setText("(1 - {})".format(ccdImageView.GetAoiMax().height))
        for item in ["none", "trace window", "file"]:
            self.ui.diagnoseOutputCombox.addItem(item)
        self.ui.diagnoseOutputCombox.setCurrentIndex(self.ccdOptionProperty["debugPrint"])
        self.ui.saveTargetImageCheckbox.setChecked(self.ccdOptionProperty["saveTargetImage"])
        strIPList = self.ccdOptionProperty["cameraIP"].split(".")
        self.ui.IPHeadEdit.setValue(int(strIPList[0]))
        self.ui.IPSecondEdit.setValue(int(strIPList[1]))
        self.ui.IPThirdEdit.setValue(int(strIPList[2]))
        self.ui.IPEndEdit.setValue(int(strIPList[3]))
        # self.ui.cameraPortEdit.setValue(self.ccdOptionProperty["cameraPort"])
        self.ui.flip180Checkbox.stateChanged.connect(self.on_flip180)
        self.ui.waitToBeInPosCheckbox.stateChanged.connect(self.on_waitToBeInPos)
        self.ui.subPixelcheckBox.stateChanged.connect(self.on_subPixel)
        for radioBtn in [self.ui.modRadioBtn, self.ui.patRadioBtn]:
            radioBtn.clicked.connect(self.on_selectModelFindAlgorithm)
        self.ui.saveTargetImageCheckbox.stateChanged.connect(self.on_saveTargetImage)
        self.ui.inPosErrMaxEdit.editingFinished2.connect(self.on_setInPosErrMax)
        self.ui.timeWaitToGrabEdit.editingFinished2.connect(self.on_setTimeWaitToGrab)
        self.ui.openDoorDelayEdit.editingFinished2.connect(self.on_setOpenDoorDelay)
        self.ui.closeDoorDelayEdit.editingFinished2.connect(self.on_setCloseDoorDelay)
        self.ui.grabTimeoutEdit.editingFinished2.connect(self.on_setGrabTimeout)
        self.ui.ccdFieldXEdit.editingFinished2.connect(self.on_setCcdFieldX)
        self.ui.ccdFieldYEdit.editingFinished2.connect(self.on_setCcdFieldY)
        self.ui.diagnoseOutputCombox.currentTextChanged.connect(self.on_selectDiagnoseOutput)
        self.ui.deviceTypeCombox.currentTextChanged.connect(self.on_selectCameraType)
        self.ui.IPHeadEdit.editingFinished2.connect(self.on_setCameraIP)
        self.ui.IPSecondEdit.editingFinished2.connect(self.on_setCameraIP)
        self.ui.IPThirdEdit.editingFinished2.connect(self.on_setCameraIP)
        self.ui.IPEndEdit.editingFinished2.connect(self.on_setCameraIP)
        # self.ui.cameraPortEdit.editingFinished2.connect(self.on_setCameraPort)
        self.ui.workDirEdit.setText("{}".format(ccdImageView.GetConfigPath()))
        self.ui.workDirEdit.setEnabled(False)
        self.ui.openPathBtn.setEnabled(False)
        # self.ui.workDirEdit.setText("{}".format(ccdImageView.GetConfigPath()))
        # self.ui.workDirEdit.editingFinished.connect(self.on_setWorkDir)
        # self.ui.openPathBtn.clicked.connect(self.on_openPath)

    def getCCDOptionProperty(self):
        # tab1
        self.ccdOptionProperty["ignoreCCD"] = self.ccdOption.bIgnoreCcd
        self.ccdOptionProperty["ignoreSkewPt"] = self.ccdOption.bIgnoreSkewPoint
        self.ccdOptionProperty["ignoreLocPoint"] = self.ccdOption.bIgnoreLocPoint
        self.ccdOptionProperty["ignoreFailed"] = self.ccdOption.bIgnoreFailed
        self.ccdOptionProperty["manualAssistRecognize"] = self.ccdOption.bManualAssistRecognize
        self.ccdOptionProperty["gain"] = self.ccdOption.nGain
        self.ccdOptionProperty["exposureTime"] = self.ccdOption.nExposureTime
        self.ccdOptionProperty["drawCross"] = self.ccdOption.bDrawCross
        self.ccdOptionProperty["drawFrameCircle"] = self.ccdOption.bDrawFrameCircle
        self.ccdOptionProperty["drawRoi"] = self.ccdOption.bDrawRoi
        self.ccdOptionProperty["defaultThreshold"] = self.ccdOption.nDefaultThreshold
        self.ccdOptionProperty["defaultOffsetMax"] = self.ccdOption.nDefaultOffsetMax
        self.ccdOptionProperty["defaultAngleMax"] = self.ccdOption.nDefaultAngleMax
        # tab2
        self.ccdOptionProperty["skewSinglePiece"] = self.ccdSetting.bSkewSinglePiece
        self.ccdOptionProperty["useLocPoint2"] = self.ccdSetting.bUseLocPoint2
        self.ccdOptionProperty["use4PtRect"] = self.ccdSetting.b4PointRect
        self.ccdOptionProperty["machiningUseNcFile"] = self.ccdOption.bMachiningUseNcFile
        self.ccdOptionProperty["compSkewPoint"] = self.ccdOption.bCompSkewPoint
        self.ccdOptionProperty["skewPointsAngle"] = self.ccdSetting.nSkewPointsAngle
        # tab3
        self.ccdOptionProperty["flip180"] = self.ccdOption.bFlip180
        self.ccdOptionProperty["waitToBeInPos"] = self.ccdOption.bWaitToBeInPos
        self.ccdOptionProperty["inPosErrMax"] = self.ccdOption.nInPosErrMax
        self.ccdOptionProperty["timeWaitToGrab"] = self.ccdOption.nTimeWaitToGrab
        self.ccdOptionProperty["openDoorDelay"] = self.ccdOption.nOpenDoorDelay
        self.ccdOptionProperty["closeDoorDelay"] = self.ccdOption.nCloseDoorDelay
        self.ccdOptionProperty["grabTimeout"] = self.ccdOption.nGrabTimeout
        self.ccdOptionProperty["grabberType"] = self.ccdOption.nGrabberType
        self.ccdOptionProperty["modelFindAlgorithm"] = self.ccdOption.nModelFindAlgorithm
        self.ccdOptionProperty["subPixel"] = self.ccdOption.bSubpixel
        self.ccdOptionProperty["CCDFieldX"] = self.ccdOption.nCcdFieldX
        self.ccdOptionProperty["CCDFieldY"] = self.ccdOption.nCcdFieldY
        self.ccdOptionProperty["debugPrint"] = self.ccdOption.nDebugPrint
        self.ccdOptionProperty["saveTargetImage"] = self.ccdOption.bSaveTargetImage
        self.ccdOptionProperty["cameraIP"] = self.ccdOption.strCameraIP
        # self.ccdOptionProperty["cameraPort"] = self.ccdOption.nCameraPort

    def setCCDOptionProperty(self):
        self.ccdOption.bIgnoreCcd = self.ccdOptionProperty["ignoreCCD"]
        self.ccdOption.bIgnoreSkewPoint = self.ccdOptionProperty["ignoreSkewPt"]
        self.ccdOption.bIgnoreLocPoint = self.ccdOptionProperty["ignoreLocPoint"]
        self.ccdOption.bIgnoreFailed = self.ccdOptionProperty["ignoreFailed"]
        self.ccdOption.bManualAssistRecognize = self.ccdOptionProperty["manualAssistRecognize"]
        self.ccdOption.nGain = self.ccdOptionProperty["gain"]
        self.ccdOption.nExposureTime = self.ccdOptionProperty["exposureTime"]
        self.ccdOption.bDrawCross = self.ccdOptionProperty["drawCross"]
        self.ccdOption.bDrawFrameCircle = self.ccdOptionProperty["drawFrameCircle"]
        self.ccdOption.bDrawRoi = self.ccdOptionProperty["drawRoi"]
        self.ccdOption.nDefaultThreshold = self.ccdOptionProperty["defaultThreshold"]
        self.ccdOption.nDefaultOffsetMax = self.ccdOptionProperty["defaultOffsetMax"]
        self.ccdOption.nDefaultAngleMax = self.ccdOptionProperty["defaultAngleMax"]
        self.ccdSetting.bSkewSinglePiece = self.ccdOptionProperty["skewSinglePiece"]
        self.ccdSetting.bUseLocPoint2 = self.ccdOptionProperty["useLocPoint2"]
        self.ccdSetting.b4PointRect = self.ccdOptionProperty["use4PtRect"]
        self.ccdOption.bMachiningUseNcFile = self.ccdOptionProperty["machiningUseNcFile"]
        self.ccdOption.bCompSkewPoint = self.ccdOptionProperty["compSkewPoint"]
        self.ccdSetting.nSkewPointsAngle = self.ccdOptionProperty["skewPointsAngle"]
        self.ccdOption.bFlip180 = self.ccdOptionProperty["flip180"]
        self.ccdOption.bWaitToBeInPos = self.ccdOptionProperty["waitToBeInPos"]
        self.ccdOption.nInPosErrMax = self.ccdOptionProperty["inPosErrMax"]
        self.ccdOption.nTimeWaitToGrab = self.ccdOptionProperty["timeWaitToGrab"]
        self.ccdOption.nOpenDoorDelay = self.ccdOptionProperty["openDoorDelay"]
        self.ccdOption.nCloseDoorDelay = self.ccdOptionProperty["closeDoorDelay"]
        self.ccdOption.nGrabTimeout = self.ccdOptionProperty["grabTimeout"]
        self.ccdOption.nGrabberType = self.ccdOptionProperty["grabberType"]
        self.ccdOption.nModelFindAlgorithm = self.ccdOptionProperty["modelFindAlgorithm"]
        self.ccdOption.bSubpixel = self.ccdOptionProperty["subPixel"]
        self.ccdOption.nCcdFieldX = self.ccdOptionProperty["CCDFieldX"]
        self.ccdOption.nCcdFieldY = self.ccdOptionProperty["CCDFieldY"]
        self.ccdOption.nDebugPrint = self.ccdOptionProperty["debugPrint"]
        self.ccdOption.bSaveTargetImage = self.ccdOptionProperty["saveTargetImage"]
        self.ccdOption.strCameraIP = self.ccdOptionProperty["cameraIP"]
        # self.ccdOption.nCameraPort = self.ccdOptionProperty["cameraPort"]

    # Tab1
    def on_ignoreCCD(self, state):
        if state == QtCore.Qt.Checked:
            self.ccdOptionProperty["ignoreCCD"] = True
        else:
            self.ccdOptionProperty["ignoreCCD"] = False

    def on_ignoreSkewPoint(self, state):
        if state == QtCore.Qt.Checked:
            self.ccdOptionProperty["ignoreSkewPt"] = True
        else:
            self.ccdOptionProperty["ignoreSkewPt"] = False

    def on_ignoreLocPoint(self, state):
        if state == QtCore.Qt.Checked:
            self.ccdOptionProperty["ignoreLocPoint"] = True
        else:
            self.ccdOptionProperty["ignoreLocPoint"] = False

    def on_ignoreFailed(self, state):
        if state == QtCore.Qt.Checked:
            self.ccdOptionProperty["ignoreFailed"] = True
        else:
            self.ccdOptionProperty["ignoreFailed"] =  False

    def on_manualAssistRecognize(self, state):
        if state == QtCore.Qt.Checked:
            self.ccdOptionProperty["manualAssistRecognize"] = True
        else:
            self.ccdOptionProperty["manualAssistRecognize"] = False

    def on_setCCDGain(self):
        self.ccdOptionProperty["gain"] = self.ui.ccdGainEdit.value()

    def on_setCCDExposureTime(self):
        self.ccdOptionProperty["exposureTime"] = self.ui.ccdExposureTimeEdit.value()

    def on_drawCross(self, state):
        if state == QtCore.Qt.Checked:
            self.ccdOptionProperty["drawCross"] = True
        else:
            self.ccdOptionProperty["drawCross"] = False

    def on_drawFrameCircle(self, state):
        if state == QtCore.Qt.Checked:
            self.ccdOptionProperty["drawFrameCircle"] = True
        else:
            self.ccdOptionProperty["drawFrameCircle"] = False

    def on_drawROI(self, state):
        if state == QtCore.Qt.Checked:
            self.ccdOptionProperty["drawRoi"] = True
        else:
            self.ccdOptionProperty["drawRoi"] = False

    def on_setDefaultThreshold(self):
        self.ccdOptionProperty["defaultThreshold"] = self.ui.defaultThresholdEdit.value()

    def on_setDefaultOffsetMax(self):
        self.ccdOptionProperty["defaultOffsetMax"] = self.ui.maxAllowedErrorEdit.value()

    def on_setDefaultAngleMax(self):
        self.ccdOptionProperty["defaultAngleMax"] = self.ui.maxAllowedAngleErrorEdit.value()

    def on_cameraSetting(self):
        pass

    # tab2
    def on_skewSinglePiece(self, state):
        if state == QtCore.Qt.Checked:
            self.ccdOptionProperty["skewSinglePiece"] = True
        else:
            self.ccdOptionProperty["skewSinglePiece"] = False

    def on_useLocPoint2(self,state):
        if state == QtCore.Qt.Checked:
            self.ccdOptionProperty["useLocPoint2"] = True
            self.ui.fourPointsRectCheckbox.setEnabled(True)
        else:
            self.ccdOptionProperty["useLocPoint2"] = False
            self.ccdOptionProperty["use4PtRect"] = False
            self.ui.fourPointsRectCheckbox.setChecked(False)
            self.ui.fourPointsRectCheckbox.setEnabled(False)

    def on_fourPointsRect(self, state):
        if state == QtCore.Qt.Checked:
            self.ccdOptionProperty["use4PtRect"] = True
        else:
            self.ccdOptionProperty["use4PtRect"] = False

    def on_machineUseNcFile(self,state):
        if state == QtCore.Qt.Checked:
            self.ccdOptionProperty["machiningUseNcFile"] = True
        else:
            self.ccdOptionProperty["machiningUseNcFile"] = False

    def on_skewPointCompensation(self,state):
        if state == QtCore.Qt.Checked:
            self.ccdOptionProperty["compSkewPoint"] = True
        else:
            self.ccdOptionProperty["compSkewPoint"] = False

    def on_selectSkewPointAngle(self):
        _logger.debug("choose Skew P1 P2 Angle")
        if self.sender() == self.ui.horizentalRadioBtn:
            self.ccdOptionProperty["skewPointsAngle"] = 0.0
            self.ui.skewPointsAngleEdit.setEnabled(False)
        elif self.sender() == self.ui.verticalRadioBtn:
            self.ccdOptionProperty["skewPointsAngle"] = 90.0
            self.ui.skewPointsAngleEdit.setEnabled(False)
        elif self.sender() == self.ui.angleRadioBtn:
            self.ui.skewPointsAngleEdit.setEnabled(True)
            # self.ccdOptionProperty["skewPointsAngle"] = self.ui.anglePt1Pt2Edit.value()

    def on_setSkewPointsAngle(self):
        skewPointsAngle = self.ui.skewPointsAngleEdit.value()
        if int(skewPointsAngle) == 0:
            self.ui.horizentalRadioBtn.setChecked(True)
        elif int(skewPointsAngle) == 90:
            self.ui.verticalRadioBtn.setChecked(True)
        else:
            self.ui.angleRadioBtn.setChecked(True)
            self.ccdOptionProperty["skewPointsAngle"] = skewPointsAngle

    # tab3
    def on_flip180(self, state):
        if state == QtCore.Qt.Checked:
            self.ccdOptionProperty["flip180"] = True
        else:
            self.ccdOptionProperty["flip180"] = False

    def on_waitToBeInPos(self, state):
        if state == QtCore.Qt.Checked:
            self.ccdOptionProperty["waitToBeInPos"] = True
        else:
            self.ccdOptionProperty["waitToBeInPos"] = False

    def on_setInPosErrMax(self):
        self.ccdOptionProperty["inPosErrMax"] = self.ui.inPosErrMaxEdit.value()

    def on_setTimeWaitToGrab(self):
        self.ccdOptionProperty["timeWaitToGrab"] = self.ui.timeWaitToGrabEdit.value()

    def on_setOpenDoorDelay(self):
        self.ccdOptionProperty["openDoorDelay"] = self.ui.openDoorDelayEdit.value()

    def on_setCloseDoorDelay(self):
        self.ccdOptionProperty["closeDoorDelay"] = self.ui.closeDoorDelayEdit.value()

    def on_setGrabTimeout(self):
        self.ccdOptionProperty["grabTimeout"] = self.ui.grabTimeoutEdit.value()

    def on_selectCameraType(self, item_text):
        _logger.debug("CameraType = {}".format(item_text))
        if item_text == "Basler":
            self.ccdOptionProperty["grabberType"] = _cnc.GRABBER_TYPE_PYLON
        elif item_text == "PtGrey":
            self.ccdOptionProperty["grabberType"] = _cnc.GRABBER_TYPE_PTGREY
        elif item_text == "GFocus":
            self.ccdOptionProperty["grabberType"] = _cnc.GRABBER_TYPE_GFOCUS
        elif item_text == "UNKNOWN":
            self.ccdOptionProperty["grabberType"] = _cnc.GRABBER_TYPE_UNKNOWN

    def on_selectModelFindAlgorithm(self):
        if self.sender() is self.ui.modRadioBtn:
            self.ccdOptionProperty["modelFindAlgorithm"] = 0
        elif self.sender() is self.ui.patRadioBtn:
            self.ccdOptionProperty["modelFindAlgorithm"] = 1

    def on_subPixel(self, state):
        if state:
            self.ccdOptionProperty["subPixel"] = True
        else:
            self.ccdOptionProperty["subPixel"] = False

    def on_setCcdFieldX(self):
        ccdFiledX = self.ui.ccdFieldXEdit.value()
        if ccdFiledX > ccdImageView.GetAoiMax().width:
            _logger.warning(_translate("ccdoptiondlg", "Set image AOI width failed, AOI width is out of range"))
            self.ui.ccdFieldXEdit.setValue(self.ui.ccdFieldXEdit.lastValue)
            return
        self.ccdOptionProperty["CCDFieldX"] = self.ui.ccdFieldXEdit.value()

    def on_setCcdFieldY(self):
        ccdFiledY = self.ui.ccdFieldYEdit.value()
        if ccdFiledY > ccdImageView.GetAoiMax().height:
            _logger.warning(_translate("ccdoptiondlg", "Set image AOI height failed, AOI height is out of range"))
            self.ui.ccdFieldYEdit.setValue(self.ui.ccdFieldYEdit.lastValue)
            return
        self.ccdOptionProperty["CCDFieldY"] = self.ui.ccdFieldYEdit.value()

    def on_selectDiagnoseOutput(self, item_text):
        if item_text == "none":
            self.ccdOptionProperty["debugPrint"] = 0
        elif item_text == "trace window":
            self.ccdOptionProperty["debugPrint"] = 1
        elif item_text == "file":
            self.ccdOptionProperty["debugPrint"] = 2

    def on_saveTargetImage(self, state):
        if state == QtCore.Qt.Checked:
            self.ccdOptionProperty["saveTargetImage"] = True
        else:
            self.ccdOptionProperty["saveTargetImage"] = False

    def on_setCameraIP(self):
        cameraIP = "{}.{}.{}.{}".format(self.ui.IPHeadEdit.value(), self.ui.IPSecondEdit.value(),
                                        self.ui.IPThirdEdit.value(), self.ui.IPEndEdit.value())
        self.ccdOptionProperty["cameraIP"] = cameraIP

    # def on_setCameraPort(self):
    #     self.ccdOptionProperty["cameraPort"] = self.ui.cameraPortEdit.value()

    # def on_setWorkDir(self):
    #     workDir = self.ui.workDirEdit.text()
    #     if workDir:
    #         ccdImageView.SetConfigPath(workDir)
        # self.ccdSetting.inFilePath = self.ui.workDirEdit.text()

    # def on_openPath(self):
    #     fileName, fileType = QFileDialog.getOpenFileName(self, "选择文件", basic.ncDir, "Select Files (*.*)")
    #     if fileName:
    #         self.ui.workDirEdit.setText(fileName)
    #         ccdImageView.SetConfigPath(fileName)
            # self.ccdSetting.inFilePath = fileName

    def on_Apply(self):
        self.setCCDOptionProperty()
        self.optionModify.SetCcdParamChanged(_cnc.CCD_PARAM_OPTION)

    def on_OK(self):
        self.on_Apply()
        self.close()

    def on_Cancel(self):
        self.close()


def showCCDOptionDlg():
    basic.showWindow(CCDOptionDlg)




# ccdmaskdlg.py
# 
# 
import logging
from PyQt5 import QtWidgets, QtCore
from .ccdview import ccdImageView
from .ccdcalibratedlg import ccdTemplateDlg
import basic
import _cnc

_logger = logging.getLogger(__name__)
_translate = QtCore.QCoreApplication.translate

class CCDMaskDlg(QtWidgets.QDialog):

    instance_count = 0
    def __init__(self, path_index=0, parent=None):
        super(CCDMaskDlg, self).__init__(parent)
        CCDMaskDlg.instance_count += 1
        self.ui = basic.loadUi(self, ":/common/ccd/CCDmask.ui")
        self.currentPath = path_index
        # _logger.info("ccd mask current path = {}".format(self.currentPath))
        self.ccdSetting = ccdImageView.GetCcdSetting(self.currentPath)
        self.ccdMaskModify = _cnc.CCcdSettingsDlg()
        self.ui.markTab.setCurrentIndex(0)
        self.maskPropertyDict = {}
        self.getMaskProperty()
        self.initUi()
        self.updateUi()

    def initUi(self):
        self.ui.markTab.tabBarClicked.connect(self.updateMaskTab)
        ccdTemplateDlg.ccdTemplateDlgHiddenSignal.connect(self.updateTemplateNo)
        self.ui.templateNoP1Edit.editingFinished2.connect(self.on_setTemplateNo)
        self.ui.templateNoP2Edit.editingFinished2.connect(self.on_setTemplateNo)
        self.ui.templateNoP3Edit.editingFinished2.connect(self.on_setTemplateNo)
        self.ui.templateNoP4Edit.editingFinished2.connect(self.on_setTemplateNo)
        self.ui.selectTemplateP1Btn.clicked.connect(self.on_selectTemplate)
        self.ui.selectTemplateP2Btn.clicked.connect(self.on_selectTemplate)
        self.ui.selectTemplateP3Btn.clicked.connect(self.on_selectTemplate)
        self.ui.selectTemplateP4Btn.clicked.connect(self.on_selectTemplate)
        self.ui.goToPointP1Btn.clicked.connect(self.on_goToPointPos)
        self.ui.goToPointP2Btn.clicked.connect(self.on_goToPointPos)
        self.ui.goToPointP3Btn.clicked.connect(self.on_goToPointPos)
        self.ui.goToPointP4Btn.clicked.connect(self.on_goToPointPos)
        self.ui.skewSinglePieceCheckBox.stateChanged.connect(self.on_skewSinglePiece)
        for radio in [self.ui.horizentalRadioBtn, self.ui.verticalRadioBtn, self.ui.angleWithRadioBtn]:
            radio.clicked.connect(self.on_selectLocationAngle)
        self.ui.angleP1P2Edit.editingFinished2.connect(self.on_setAngleP1P2)
        self.ui.useLocPt2CheckBox.stateChanged.connect(self.on_useLocPt2)
        self.ui.use4PtRectCheckBox.stateChanged.connect(self.on_use4PtRect)
        self.ui.OK_Btn.clicked.connect(self.on_OK)
        self.ui.Cancel_Btn.clicked.connect(self.on_Cancel)

    def updateMaskTab(self):
        if self.maskPropertyDict["useLocPt2"]:
            self.ui.templateNoP4Edit.setEnabled(True)
            self.ui.selectTemplateP4Btn.setEnabled(True)
            self.ui.goToPointP4Btn.setEnabled(True)
        else:
            self.ui.templateNoP4Edit.setEnabled(False)
            self.ui.selectTemplateP4Btn.setEnabled(False)
            self.ui.goToPointP4Btn.setEnabled(False)

    def updateTemplateNo(self, template_no):
        currentTab = self.ui.markTab.currentIndex()
        if currentTab == 0:
            self.maskPropertyDict["templateNoSkewPt1"] = template_no
        elif currentTab == 1:
            self.maskPropertyDict["templateNoSkewPt2"] = template_no
        elif currentTab == 2:
            self.maskPropertyDict["templateNoSinglePt1"] = template_no
        elif currentTab == 3:
            self.maskPropertyDict["templateNoSinglePt2"] = template_no
        self.updateUi()

    def on_setTemplateNo(self):
        templateNo = self.sender().value()
        if ccdImageView.GetModelMgr().GetModelByModelNo(templateNo):
            if self.sender() == self.ui.templateNoP1Edit:
                self.maskPropertyDict["templateNoSkewPt1"] = templateNo
            elif self.sender() == self.ui.templateNoP2Edit:
                self.maskPropertyDict["templateNoSkewPt2"] = templateNo
            elif self.sender() == self.ui.templateNoP3Edit:
                self.maskPropertyDict["templateNoSinglePt1"] = templateNo
            elif self.sender() == self.ui.templateNoP4Edit:
                self.maskPropertyDict["templateNoSinglePt2"] = templateNo
        else:
            _logger.error(_translate("ccdmaskdlg", "{}template is not exist, please try other template.").format(templateNo))
            self.sender().setValue(self.sender().lastValue)

    def getMaskProperty(self):
        self.maskPropertyDict["templateNoSkewPt1"] = self.ccdSetting.GetGrabPointModelNo(_cnc.GRAB_P1)
        self.maskPropertyDict["skewSinglePiece"] = self.ccdSetting.bSkewSinglePiece
        self.maskPropertyDict["templateNoSkewPt2"] = self.ccdSetting.GetGrabPointModelNo(_cnc.GRAB_P2)
        self.maskPropertyDict["angleWithSkewPt1"] = self.ccdSetting.nSkewPointsAngle
        self.maskPropertyDict["templateNoSinglePt1"] = self.ccdSetting.GetGrabPointModelNo(_cnc.GRAB_P3)
        self.maskPropertyDict["templateNoSinglePt2"] = self.ccdSetting.GetGrabPointModelNo(_cnc.GRAB_P4)
        self.maskPropertyDict["useLocPt2"] = self.ccdSetting.bUseLocPoint2
        self.maskPropertyDict["use4PtRect"] = self.ccdSetting.b4PointRect

    def setMaskProperty(self):
        self.ccdSetting.SetGrabPointModelNo(_cnc.GRAB_P1, self.maskPropertyDict["templateNoSkewPt1"])
        self.ccdSetting.bSkewSinglePiece = self.maskPropertyDict["skewSinglePiece"]
        self.ccdSetting.SetGrabPointModelNo(_cnc.GRAB_P2, self.maskPropertyDict["templateNoSkewPt2"])
        self.ccdSetting.nSkewPointsAngle = self.maskPropertyDict["angleWithSkewPt1"]
        self.ccdSetting.SetGrabPointModelNo(_cnc.GRAB_P3, self.maskPropertyDict["templateNoSinglePt1"])
        self.ccdSetting.SetGrabPointModelNo(_cnc.GRAB_P4, self.maskPropertyDict["templateNoSinglePt2"])
        self.ccdSetting.bUseLocPoint2 = self.maskPropertyDict["useLocPt2"]
        self.ccdSetting.b4PointRect = self.maskPropertyDict["use4PtRect"]

    def updateUi(self):
        self.ui.templateNoP1Edit.setValue(self.maskPropertyDict.get("templateNoSkewPt1", -1))
        self.ui.skewSinglePieceCheckBox.setChecked(self.maskPropertyDict.get("skewSinglePiece", False))
        self.ui.templateNoP2Edit.setValue(self.maskPropertyDict.get("templateNoSkewPt2", -1))
        self.ui.templateNoP3Edit.setValue(self.maskPropertyDict.get("templateNoSinglePt1", -1))
        self.ui.templateNoP4Edit.setValue(self.maskPropertyDict.get("templateNoSinglePt2", -1))
        self.updateAngleP1P2Ui(self.maskPropertyDict.get("angleWithSkewPt1", -1.0))
        self.ui.templateNoP3Edit.setValue(self.maskPropertyDict.get("templateNoSinglePt1", -1))
        self.ui.templateNoP4Edit.setValue(self.maskPropertyDict.get("templateNoSinglePt2", -1))
        self.ui.useLocPt2CheckBox.setChecked(self.maskPropertyDict.get("useLocPt2", False))
        self.ui.use4PtRectCheckBox.setChecked(self.maskPropertyDict.get("use4PtRect", False))
        self.updateMaskTab()

    def updateAngleP1P2Ui(self, angle):
        if abs(angle - 0) < 0.0001:
            self.ui.horizentalRadioBtn.setChecked(True)
            self.ui.angleP1P2Edit.setEnabled(False)
        elif int(angle) == 90:
            self.ui.verticalRadioBtn.setChecked(True)
            self.ui.angleP1P2Edit.setEnabled(False)
        else:
            self.ui.angleP1P2Edit.setEnabled(True)
            self.ui.angleWithRadioBtn.setChecked(True)

    def on_selectTemplate(self):
        basic.showCCDTemplateDlg()

    def on_goToPointPos(self):
        basic.mdi('G65 P<CCD_GOTO_POINT>')

    def on_skewSinglePiece(self, state):
        if state == QtCore.Qt.Checked:
            self.maskPropertyDict["skewSinglePiece"] = True
        else:
            self.maskPropertyDict["skewSinglePiece"] = False

    def on_selectLocationAngle(self):
        if self.sender() == self.ui.horizentalRadioBtn:
            self.ui.angleP1P2Edit.setEnabled(False)
            self.maskPropertyDict["angleWithSkewPt1"] = 0.0
        elif self.sender() == self.ui.verticalRadioBtn:
            self.ui.angleP1P2Edit.setEnabled(False)
            self.maskPropertyDict["angleWithSkewPt1"] = 90.0
        elif self.sender() == self.ui.angleWithRadioBtn:
            self.ui.angleP1P2Edit.setEnabled(True)

    def on_setAngleP1P2(self):
        self.maskPropertyDict["angleWithSkewPt1"] = self.ui.angleP1P2Edit.value()

    def on_useLocPt2(self, state):
        if state == QtCore.Qt.Checked:
            self.maskPropertyDict["useLocPt2"] = True
        else:
            self.maskPropertyDict["useLocPt2"] = False
        self.updateMaskTab()

    def on_use4PtRect(self, state):
        if state == QtCore.Qt.Checked:
            self.maskPropertyDict["use4PtRect"] = True
        else:
            self.maskPropertyDict["use4PtRect"] = False

    def on_OK(self):
        if self.maskPropertyDict:
            self.setMaskProperty()
            self.ccdMaskModify.SetCcdParamChanged(_cnc.CCD_PARAM_SETTING)
        self.close()

    def on_Cancel(self):
        self.close()

    def done(self, result):
        super(CCDMaskDlg, self).done(result)
        CCDMaskDlg.instance_count -= 1


def showCCDMaskDlg(current_path=0, parent=None):
    if CCDMaskDlg.instance_count < 1:
        dlg = CCDMaskDlg(current_path, parent)
        dlg.setGeometry(basic.mainWindow.x() + basic.mainWindow.width()/2 - dlg.width()/2,
                        basic.mainWindow.y() + basic.mainWindow.height()/2 - dlg.height()/2,
                        dlg.width(),
                        dlg.height())
        dlg.show()                     

## ccdctrldlg.py
# 
# 
import logging
import math
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import basic
from  basic import R, unit
from .ccdview import ccdImageView, ccd_view_frame
from . import ccdtemplatedlg
from . import ccdoriginposdlg
from . import productarraydlg
from . import multipathlayoutdlg
from . import multipanelprocessdlg
from . import ccdoptiondlg
from . import ccdpropertydlg
from . import ccdcalibratedlg
from . import ccdTemplateBase
import _cnc


_logger = logging.getLogger(__name__)
_translate = QtCore.QCoreApplication.translate

class CCDCtrlDlg(QtWidgets.QDialog):

    def __init__(self):
        super(CCDCtrlDlg, self).__init__()
        self.ui = basic.loadUi(self, ":/common/ccd/CCDctrldlg.ui")
        self.initManualTab()
        self.initSettingTab()
        self.ui.ccdCtrlTabWidget.setCurrentIndex(0)
        basic.signal_UpdateUi.connect(self.updateUi)

    def initManualTab(self):
        self.setUIEnabled(False)
        self.ui.middleTemplate.setChecked(True)
        self.trailCut = ccdImageView.GetCcdTrialCut()
        self.ui.startPosEdit.setValue(self.trailCut.nStart)
        self.ui.endPosEdit.setValue(self.trailCut.nEnd)
        self.ui.trialCuttingCheckBox.setChecked(self.trailCut.bEnable)
        self.ui.grabImageBtn.clicked.connect(self.on_grabImage)
        self.ui.grabTemplateBtn.clicked.connect(self.on_grabTemplate)
        self.ui.focusTipsBtn.clicked.connect(self.on_focusTips)
        for radioBtn in [self.ui.smallTemplate, self.ui.middleTemplate,
                         self.ui.largeTemplate, self.ui.diyTemplate]:
            radioBtn.clicked.connect(self.on_selectTemplateSize)
        self.ui.ptFirstBtn.clicked.connect(self.on_recordFirstPoint)
        self.ui.ptSecondBtn.clicked.connect(self.on_recordSecondPoint)
        self.ui.backToFocusBtn.clicked.connect(self.on_backToFocus)
        self.ui.ccdGateBtn.clicked.connect(self.on_CCDGateOnOff)
        self.ui.setTemplateSizeBtn.clicked.connect(self.on_DIYTemplateSize)
        self.ui.setSearchRangeBtn.clicked.connect(self.on_setSearchRange)

    def initSettingTab(self):
        self.ui.ccdTemplateBtn.clicked.connect(self.on_showCCDTemplateDlg)
        self.ui.ccdHomePosBtn.clicked.connect(ccdoriginposdlg.showCCDOriginPosDlg)
        self.ui.ccdProductArrayBtn.clicked.connect(
            productarraydlg.showProductArrayDlg)
        self.ui.multiPathLayoutBtn.clicked.connect(
            multipathlayoutdlg.showMultiPathLayoutDlg)
        self.ui.multiPlateProcessBtn.clicked.connect(
            multipanelprocessdlg.showMultiPanelProcessDlg)
        self.ui.ccdOptionBtn.clicked.connect(ccdoptiondlg.showCCDOptionDlg)
        self.ui.ccdPropertyBtn.clicked.connect(
            ccdpropertydlg.showCCDPropertyDlg)
        self.ui.ccdCalibrationBtn.clicked.connect(
            ccdcalibratedlg.showCCDCalibrateDlg)

    def updateUi(self):
        if basic.Auth_Level() > 10:
            self.ui.ccdOptionBtn.setEnabled(False)
            self.ui.ccdPropertyBtn.setEnabled(False)

    def setUIEnabled(self, enabled):
        self.ui.grabTemplateBtn.setEnabled(enabled)
        self.ui.focusTipsBtn.setEnabled(enabled)
        self.ui.backToFocusBtn.setEnabled(enabled)
        self.ui.setTemplateSizeBtn.setEnabled(enabled)
        self.ui.setSearchRangeBtn.setEnabled(enabled)
        if not self.ui.grabTemplateBtn.isEnabled():
            self.ui.grabTemplateBtn.setChecked(False)
        if not self.ui.focusTipsBtn.isEnabled():
            self.ui.focusTipsBtn.setChecked(False)

    def on_grabImage(self):
        _logger.debug("garb image button was clicked")
        if ccdImageView.IsCcdOpen(): # 关闭CCD
            self.setUIEnabled(False)
            status = ccdImageView.CloseCcdDevice(False)
            # _logger.info(_translate("ccdctrldlg", "status = {}").format(_cnc.GetErrString(status)))
        else: # 打开CCD
            self.setUIEnabled(True)
            self.setCursor(QtCore.Qt.WaitCursor)
            status = ccdImageView.OpenCcdDevice(True)  # 参数True:是否连续取像
            # _logger.info("status = {}".format(_cnc.GetErrString(status)))
            aoiRect = ccdImageView.GetAoi()
            if aoiRect.width > 0 and aoiRect.height > 0:
                ccd_view_frame.adjustCCDViewSize(aoiRect.width, aoiRect.height)
                # _logger.info("aoi rect = {}/{}".format(aoiRect.width, aoiRect.height))
            else:
                _logger.error(_translate("ccdctrldlg", "image AOI is null"))
            self.setCursor(QtCore.Qt.ArrowCursor)

    def on_grabTemplate(self):
        _logger.debug("garb template button was clicked")
        if self.ui.focusTipsBtn.isChecked():
            self.ui.focusTipsBtn.setChecked(False)
        if ccdImageView.IsCcdOpen():
            if ccdImageView.GetCurrentOperationMode() != _cnc.CCD_OP_GRAB_MODEL:
                ccdImageView.SetOperationMode(_cnc.CCD_OP_GRAB_MODEL)
            else:
                ccdImageView.SetOperationMode(_cnc.CCD_OP_NOTHING)
        else:
            _logger.error(_translate("ccdctrldlg", "Please open CCD!"))

    def on_focusTips(self):
        _logger.debug("focus tips button was clicked")
        if self.ui.grabTemplateBtn.isChecked():
            self.ui.grabTemplateBtn.setChecked(False)
        if ccdImageView.IsCcdOpen():
            if ccdImageView.GetCurrentOperationMode() != _cnc.CCD_OP_FOCUS:
                ccdImageView.SetOperationMode(_cnc.CCD_OP_FOCUS)
            else:
                ccdImageView.SetOperationMode(_cnc.CCD_OP_NOTHING)
        else:
            _logger.error(_translate("ccdctrldlg", "Please open CCD!"))

    def on_selectTemplateSize(self):
        _logger.debug("select template size")
        if self.sender() is self.ui.smallTemplate:
            ccdImageView.SelectModelSize(_cnc.MODEL_SIZE_SMALL)
        elif self.sender() is self.ui.middleTemplate:
            ccdImageView.SelectModelSize(_cnc.MODEL_SIZE_MEDIUM)
        elif self.sender() is self.ui.largeTemplate:
            ccdImageView.SelectModelSize(_cnc.MODEL_SIZE_BIG)
        elif self.sender() is self.ui.diyTemplate:
            ccdImageView.SelectModelSize(_cnc.MODEL_SIZE_USER)

    def on_recordFirstPoint(self):
        self.firstPoint = (R[101]*unit.cnc2hmiLength, R[102]*unit.cnc2hmiLength)
        self.ui.disTextBrowser.setText(" ")

    def on_recordSecondPoint(self):
        if not hasattr(self, "firstPoint"):
            _logger.error(_translate("ccdctrldlg", "Please record first point"))
            return
        self.secondPoint = (R[101]*unit.cnc2hmiLength, R[102]*unit.cnc2hmiLength)
        distance = math.sqrt(math.pow((self.firstPoint[0]-self.secondPoint[0]), 2) + \
                             math.pow((self.firstPoint[1]-self.secondPoint[1]), 2))
        self.ui.disTextBrowser.setText(_translate("ccdctrldlg", "Dis = {:.3f}").format(distance))

    def on_backToFocus(self):
        basic.mdi('G65 P<CCD_FOCUS>')

    def on_CCDGateOnOff(self):
        if R[1406, 0]:
            R[1406, 0] = 0
        else:
            R[1406, 0] = 1

    def on_DIYTemplateSize(self):
        if ccdImageView.IsCcdOpen():
            ccdTemplateBase.showDIYTemplateSizeDlg()

    def on_setSearchRange(self):
        if ccdImageView.IsCcdOpen():
            ccdTemplateBase.showSetSearchRangeDlg()

    def trialCutting(self):
        startIndex = self.ui.startPosEdit.value()
        endIndex = self.ui.endPosEdit.value()
        isTrialCutting = self.ui.trialCuttingCheckBox.isChecked()
        if startIndex > 0 and endIndex > 0 and endIndex >= startIndex:
            if isTrialCutting:
                self.trailCut.nStart = startIndex
                self.trailCut.nEnd = endIndex
                self.trailCut.bEnable = True
            else:
                self.trailCut.bEnable = False
        else:
            _logger.warning(_translate("ccdctrldlg", "start index and end index must be lager than zero,\n"
                            "and end index must larger or equal to start index"))

    def on_showCCDTemplateDlg(self):
        ccdtemplatedlg.showCCDTemplateDlg()

    # 屏蔽ESC键导致对话框退出问题
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            return


ccdCtrl_dlg = CCDCtrlDlg()

@basic.api
def getTrialCuttingInfo():
    ccdCtrl_dlg.trialCutting()



# ccdcalibratedlg.py
# 
import logging
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem
from .ccdview import ccdImageView
from .ccdtemplatedlg import ccdTemplateDlg
import basic
import _cnc

_logger = logging.getLogger(__name__)
_translate = QtCore.QCoreApplication.translate

class CalibrateTableWidget(QTableWidget):
    deleteRowSignal = QtCore.pyqtSignal(int)
    clearTableSignal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(CalibrateTableWidget, self).__init__(parent)
        self.deleteItem = QtWidgets.QAction(_translate("ccdcalibratedlg", "Delete"), self)
        self.deleteItem.triggered.connect(self.on_deleteItem)
        self.deleteAllItem = QtWidgets.QAction(_translate("ccdcalibratedlg", "DeleteAll"), self)
        self.deleteAllItem.triggered.connect(self.on_deleteAllItem)

    def contextMenuEvent(self, event):
        if self.currentItem():
            contextMenu = QtWidgets.QMenu()
            contextMenu.setStyleSheet("font-family:Droid Sans Fallback")
            contextMenu.addAction(self.deleteItem)
            contextMenu.addAction(self.deleteAllItem)
            contextMenu.exec_(event.globalPos())

    def on_deleteItem(self):
        if self.currentItem().text():
            self.deleteRowSignal.emit(self.currentRow())
            self.removeRow(self.currentRow())

    def on_deleteAllItem(self):
        self.clearTableSignal.emit()
        self.clear()


class CCDCalibrateDlg(QDialog):

    def __init__(self, parent=None):
        super(CCDCalibrateDlg, self).__init__(parent)
        self.ui = basic.loadUi(self, ":/common/ccd/CCDcalibratedlg.ui")
        self.xResolutionList = []
        self.yResolutionList = []
        if ccdTemplateDlg.templateProperty:
            self.templateNo = ccdTemplateDlg.templateProperty.get("templateNO", 0)
            self.ui.templateNoEdit.setValue(self.templateNo)
        self.ui.xMoveDisEdit.setValue(2.0)
        self.ui.yMoveDisEdit.setValue(2.0)
        self.ui.templateNoEdit.editingFinished2.connect(self.on_setTemplateNo)
        self.ui.selectTemplateBtn.clicked.connect(self.on_selectTemplate)
        self.ui.xMoveDisEdit.editingFinished2.connect(self.on_setXMoveDis)
        self.ui.yMoveDisEdit.editingFinished2.connect(self.on_setYMoveDis)
        self.ui.calibrateBtn.clicked.connect(self.on_calibrate)
        self.ui.reverseBtn.clicked.connect(self.on_reverseCalibrate)
        self.ui.calibrateXTable.deleteRowSignal.connect(self.on_deleteXTableRow)
        self.ui.calibrateYTable.deleteRowSignal.connect(self.on_deleteYTableRow)
        self.ui.calibrateXTable.clearTableSignal.connect(self.on_clearXTable)
        self.ui.calibrateYTable.clearTableSignal.connect(self.on_clearYTable)
        self.ui.CancelBtn.clicked.connect(self.on_Cancel)
        self.ui.OKBtn.clicked.connect(self.on_OK)
        # basic.signal_UpdateUi.connect(self.updateTemplateNo)
        ccdTemplateDlg.ccdTemplateDlgHiddenSignal.connect(self.updateTemplateNo)
        ccdImageView.calibrateFinishedSignal.connect(self.on_recordResolution)

    def updateTemplateNo(self, template_no):
        self.ui.templateNoEdit.setValue(template_no)
        # if ccdTemplateDlg.templateProperty:
        #     self.templateNo = ccdTemplateDlg.templateProperty.get("templateNO")

    def on_setTemplateNo(self):
        self.templateNo = self.ui.templateNoEdit.value()
        if not ccdImageView.GetModelMgr().GetModelByModelNo(self.templateNo):
            _logger.error(_translate("ccdcalibratedlg", "{}template is not exist, please try other template.").format(self.templateNo))
            self.templateNo = self.ui.templateNoEdit.lastValue
            self.ui.templateNoEdit.setValue(self.templateNo)

    def on_selectTemplate(self):
        basic.showCCDTemplateDlg()

    def on_calibrate(self):
        modelNo = self.ui.templateNoEdit.value()
        disX = self.ui.xMoveDisEdit.value()
        disY = self.ui.yMoveDisEdit.value()
        ccdImageView.StartCalibrate(modelNo, disX, disY)
        basic.mdi('G65 P<CCD_CALI>')

    def on_reverseCalibrate(self):
        modelNo = self.ui.templateNoEdit.value()
        disX = self.ui.xMoveDisEdit.value()
        disY = self.ui.yMoveDisEdit.value()
        ccdImageView.StartCalibrate(modelNo, -disX, -disY)
        basic.mdi('G65 P<CCD_CALI>')

    def on_recordResolution(self, xResolution, yResolution):
        self.xResolutionList.append(xResolution)
        self.yResolutionList.append(yResolution)
        self.updateTable(self.ui.calibrateXTable, self.xResolutionList)
        self.updateTable(self.ui.calibrateYTable, self.yResolutionList)
        self.ui.meanValueX.setValue(self.getResolution(self.xResolutionList))
        self.ui.meanValueY.setValue(self.getResolution(self.yResolutionList))

    def updateTable(self, table_obj, resolution_list):
        if resolution_list:
            rowIndex = len(resolution_list)-1
            table_obj.insertRow(rowIndex)
            newItem  = QTableWidgetItem("{:.3f}".format(resolution_list[rowIndex]))
            table_obj.setItem(rowIndex, 0, newItem)

    def getResolution(self, resolution_list):
        if resolution_list:
            sum = 0.0
            for item in resolution_list:
                sum = sum + item
            return sum/len(resolution_list)
        else:
            return 0.0

    def on_setXMoveDis(self):
        pass

    def on_setYMoveDis(self):
        pass

    def on_deleteXTableRow(self, row):
        self.xResolutionList.pop(row)
        self.ui.meanValueX.setValue(self.getResolution(self.xResolutionList))

    def on_deleteYTableRow(self, row):
        self.yResolutionList.pop(row)
        self.ui.meanValueY.setValue(self.getResolution(self.yResolutionList))

    def on_clearXTable(self):
        self.xResolutionList.clear()
        self.ui.meanValueX.setValue(self.getResolution(self.xResolutionList))

    def on_clearYTable(self):
        self.yResolutionList.clear()
        self.ui.meanValueY.setValue(self.getResolution(self.yResolutionList))

    def on_OK(self):
        # TODO: save data
        self.close()

    def on_Cancel(self):
        self.close()


def showCCDCalibrateDlg():
    basic.showWindow(CCDCalibrateDlg)

        


