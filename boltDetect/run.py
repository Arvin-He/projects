# usr/bin/python3
# -*- coding:utf-8 -*-

from boltdetectdlg import BoltDetectDlg


if __name__ == "__main__":
    boltDetectDlg = BoltDetectDlg()
    boltDetectDlgRect = boltDetectDlg.geometry()
    boltDetectDlg.setFixedSize(boltDetectDlgRect.size())
    boltDetectDlg.exec_()
