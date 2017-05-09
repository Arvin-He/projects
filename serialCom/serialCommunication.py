# -*- coding:utf-8 -*-

import serial


def initCom(com, baudrate):
    ser = serial.Serial(com, baudrate, timeout=1)


def readData():
    pass


def transformData():
    pass


def saveData():
    pass
    