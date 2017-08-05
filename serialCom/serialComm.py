# -*- coding:utf-8 -*-
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
            return False
    else:
        logger.info("{}串口已经被打开!".format(port))
    logger.info("{}串口打开成功!".format(port))
    return True


def closeCom():
    global ser
    if ser and ser.is_open:
        ser.close()
        logger.info("串口关闭!")
        return True
    else:
        logger.info("串口没有打开,不需要关闭!")
        return False


def writeData():
    global ser
    if ser and ser.is_open:
        ser.reset_input_buffer()
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
        try:
            data = ser.read(13)
            # data = bytes.fromhex('53 0b 01 01 04 30 02 b2 4a 58 09 6b 45')
            # 将bytes的内容转16进制表示的bytes
            data2 = binascii.hexlify(data)
            # 将bytes转字符串,并返回
            return data2.decode('utf-8')
        except Exception as e:
            logger.error("read data failed, {}".format(e))
            return
    else:
        logger.info("串口没有打开!")
        return None


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
    if data and len(data) > 0:
        return data[0]
    else:
        logger.error("getFlagBit wrong data, data = {}".format(data))


def getTightTorque(data):
    if data and len(data) > 5:
        data2 = data[1:5]
        data3 = int(data2) * 0.001
        return "{:.3f}".format(data3)
    else:
        logger.error("getTightTorque wrong data, data = {}".format(data))


def getTightAngle(data):
    if data and len(data) > 5:
        data2 = data[5:]
        return data2
    else:
        logger.error("getTightAngle wrong data, data = {}".format(data))

