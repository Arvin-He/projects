# -*- coding:utf-8 -*-
import serial
import binascii

from log import logger

ser = None
last_raw_data = ""


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


def readData():
    global ser, last_raw_data
    if ser and ser.is_open:
        data = ser.read(13)
        if len(data) == 13:
            # 将bytes的内容转16进制表示的bytes
            raw_data = binascii.hexlify(data).decode('utf-8')
            if raw_data != last_raw_data:
                last_raw_data = raw_data
                res = []
                res.append(raw_data)
                temp = raw_data.replace(" ", "")[14:22]
                templist = reversed([temp[i:i + 2]
                                     for i in range(0, len(temp), 2)])
                temp2 = "".join(templist)
                int_data = str(int(temp2, 16)).zfill(8)
                res.append(int_data)
                if len(int_data) == 9:
                    flag = int(int_data[0])
                    temp3 = int(int_data[1:5])
                    torque = temp3 * \
                        0.01 if temp3 in range(0, 2000) else temp3 * 0.001
                    angle = int(int_data[5:])
                    res.append(flag)
                    res.append(torque)
                    res.append(angle)
                    # print("raw_data=", raw_data)
                    # print("temp=", temp)
                    # print("reverse temp=", temp2)
                    # print("int_data = ", int_data)
                    # print("flag = ", flag)
                    # print("torque = ", torque)
                    # print("angle = ", angle)
                    # print("xxxxxxxxxxxxxx result =", res)
                    return res
    else:
        logger.error("串口没有打开!")
