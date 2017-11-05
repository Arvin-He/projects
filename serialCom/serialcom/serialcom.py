# -*- coding:utf-8 -*-
import serial
import binascii

from log import logger

ser = None
last_raw_data = ""
last_torque = ""
last_angle = ""


def openCom(port, baud_rate, time_out):
    global ser
    if ser is None:
        try:
            ser = serial.Serial(port, baud_rate, timeout=time_out)
        except serial.serialutil.SerialException as e:
            logger.error("串口{}打开失败! 错误:{}".format(port, e))
            return False
    else:
        if ser and ser.is_open:
            logger.info("{}串口已经被打开!".format(port))
            return True
        else:
            logger.error("{}串口错误,请关闭软件并检查串口!".format(port))
            ser = None
            return False
    logger.info("{}串口打开成功!".format(port))
    return True


def closeCom():
    global ser
    if ser and ser.is_open:
        ser.close()
        ser = None
        logger.info("串口关闭!")
        return True
    else:
        logger.warning("串口没有打开,不需要关闭!")
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
        logger.error("串口没有打开!")
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
            logger.error("read data failed: {}".format(e))
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



# def readData():
#     global ser, last_raw_data, last_torque, last_angle
#     if ser and ser.is_open:
#         data = ser.read(13)
#         res = []
#         if len(data) == 13:
#             # 将bytes的内容转16进制表示的bytes
#             raw_data = binascii.hexlify(data).decode('utf-8')
#             if raw_data != last_raw_data:
#                 logger.info("last_raw_data = {}".format(last_raw_data))
#                 logger.info("raw_data = {}".format(raw_data))

#                 last_raw_data = raw_data
#                 res.append(raw_data)

#                 temp = raw_data.replace(" ", "")[14:22]
#                 templist = reversed([temp[i:i + 2]
#                                      for i in range(0, len(temp), 2)])
#                 temp2 = "".join(templist)
#                 int_data = str(int(temp2, 16)).zfill(8)
#                 res.append(int_data)

#                 if len(int_data) == 9:
#                     flag = int(int_data[0])
#                     temp3 = int(int_data[1:5])
#                     torque = temp3 * 0.01 if temp3 in range(0, 2000) else temp3 * 0.001
#                     angle = int(int_data[5:])
#                     logger.info("lt = {}, la = {}, t = {}, a = {}".format(last_torque, last_angle, torque, angle))
#                     if (str(torque) != last_angle) or (str(angle) != last_angle):
#                         last_torque = str(torque)
#                         last_angle = str(angle)
#                         logger.info("{}/{}".format(torque, angle))
#                         res.append(flag)
#                         res.append(torque)
#                         res.append(angle)
#         logger.info("read_data = {}".format(res))
#         if len(res) == 5:
#             return res
#     else:
#         logger.error("串口没有打开!")