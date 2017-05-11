# -*- coding:utf-8 -*-
import os
import csv
import serial
import binascii

from logger import logger

ser = None


def openCom(port, baud_rate):
    global ser
    if ser is None:
        try:
            ser = serial.Serial(port, baud_rate)
        except serial.serialutil.SerialException as e:
            logger.error("串口{}打开失败! 错误:{}".format(port, e))
    else:
        logger.info("{}端口已经被打开!".format(port))


def closeCom():
    global ser
    if ser and ser.is_open:
        ser.close()
        logger.info("串口已经关闭!")
    else:
        logger.info("串口没有打开!")


def writeData():
    global ser
    if ser and ser.is_open:
        # 16进制转bytes
        data = bytes.fromhex('53 07 01 01 04 30 02 64 45')
        ser.write(data)
        return True
    else:
        logger.info("串口没有打开!")
        return False


# 读取字节并转换成16进制字符串
def readData():
    global ser
    if ser and ser.is_open:
        if ser.in_waiting == 13:
            data = ser.read(13)
            # data = bytes.fromhex('53 0b 01 01 04 30 02 b2 4a 58 09 6b 45')
            # 将bytes的内容转16进制表示的bytes
            data2 = binascii.hexlify(data)
            # 将bytes转字符串,并返回
            return data2.decode('utf-8')
    else:
        logger.info("串口没有打开!")


# 读到的数据字符串"53 0B  01 01 04 30 02 B2 4A 58 09 6B 45",取其中的第8~11个16进制数
# 然后将取到的16进制数作为一个整体,转换成10进制数,并返回
def transformData(data):
    if data:
        data.replace(" ", "")
        data2 = data[14:22]
        data3 = reversed([data2[i:i + 2] for i in range(0, len(data2), 2)])
        return "".join(data3)


# 将16进制的字符串转换成10进制字符串
def processData(data):
    if data:
        data2 = str(int(data, 16)).zfill(8)
        return data2


def getFlagBit(data):
    if data:
        assert len(data) == 8
        return data[0]


def getTightTorque(data):
    if data:
        assert len(data) == 8
        data2 = data[1:5]
        data3 = int(data2) * 0.001
        return "{:.3f}".format(data3)


def getTightAngle(data):
    if data:
        assert len(data) == 8
        data2 = data[5:]
        return data2


# 保存到csv文件,csv文件可以直接用excel打开
def saveCSV(data):
    if not os.path.exists(os.path.abspath("serialdata.csv")):
        with open("serialdata.csv", "w", newline="", encoding="utf-8") as csv_file:
            header = ["[Flag Bit]", "[Tight Torque]", "[Tight Angle]"]
            writer = csv.writer(csv_file, dialect=("excel"))
            writer.writerow(header)
            csv_file.close()

    with open("serialdata.csv", "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, dialect=("excel"))
        writer.writerow(data)
