# -*- coding:utf-8 -*-
import os
import serial

ser = None


def openCom(port, baud_rate):
    global ser
    if ser is None:
        ser = serial.Serial(port, baud_rate)
        if ser.is_open:
            print("{}端口打开成功!".format(port))
        else:
            print("{}端口打开失败!".format(port))
    else:
        print("{}端口已经被打开!".format(port))


def closeCom():
    global ser
    if ser.is_open:
        ser.close()
        print("串口已经关闭!")


def readData():
    global ser
    assert ser.is_open
    data = ser.readall()
    return data


def sting2hex():
    pass


def hex2string():
    pass


# 读到的数据"53 0B  01 01 04 30 02 B2 4A 58 09 6B 45",取其中的第8~11个16进制数
# 然后将取到的16进制数作为一个整体,转换成10进制数,并返回
def transformData(data):
    data_str = str(data)
    data_str.replace(" ", "")
    new_data_str = data_str[14:21]


def saveData():
    pass


