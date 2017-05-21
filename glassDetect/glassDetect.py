# usr/bin/python3
# -*- coding:utf-8 -*-

from glassdetectdlg import GlassDetectDlg


if __name__ == "__main__":
    glassDetectDlg = GlassDetectDlg()
    glassDetectDlgRect = glassDetectDlg.geometry()
    glassDetectDlg.setFixedSize(glassDetectDlgRect.size())
    glassDetectDlg.exec_()