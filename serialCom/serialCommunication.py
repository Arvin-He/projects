# -*- coding:utf-8 -*-
import os
import csv
import serial

ser = None


def openCom(port, baud_rate):
    global ser
    if ser is None:
        ser = serial.Serial(port, baud_rate)
        print(port)
        print(baud_rate)
        if ser.is_open:
            print("{}端口打开成功!".format(port))
        else:
            print("{}端口打开失败!".format(port))
    else:
        print("{}端口已经被打开!".format(port))
    # writeData()
    # print("xxxxxxxxxxx")
    # readData()


def closeCom():
    global ser
    if ser.is_open:
        ser.close()
        print("串口已经关闭!")


def writeData():
    global ser
    assert ser.is_open
    # data = "\x53\x07\x01\x01\x04\x30\x02\x64\x45".encode('utf-8')
    data = bytes.fromhex('53 07 01 01 04 30 02 64 45')
    # data = bytes([83, 7, 1, 1, 4, 48, 2, 100, 69])
    print(data)
    import binascii
    print(binascii.hexlify(data))
    ser.write(data)

def readData():
    global ser
    assert ser.is_open
    print("data = {}".format(11111))
    data = ser.read(13)
    print("data = {}".format(data))
    import binascii
    print(binascii.hexlify(data))
    # return data


def sting2hex():
    pass


def hex2string():
    pass


# 读到的数据"53 0B  01 01 04 30 02 B2 4A 58 09 6B 45",取其中的第8~11个16进制数
# 然后将取到的16进制数作为一个整体,转换成10进制数,并返回
def transformData(data):
    # 串口读到的是字节
    # str = bytes.decode(encoding='utf-8', errors='strict)
    data_str = str(data)
    data_str.replace(" ", "")
    new_data_str = data_str[14:21]


# # 保存到csv文件,csv文件可以导入到excel中去
# def saveData():
#     with open("data.csv", "w", newline="") as datacsv:
#         # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
#         csvwriter = csv.writer(datacsv, dialect=("excel"))
#         # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
#         csvwriter.writerow(["序号", "标志位", "力矩", "角度"])
#
#
# # 读取csv文件
# def readData():
#     with open("data.csv", "r", encoding="utf-8") as csvfile:
#         # 读取csv文件，返回的是迭代类型
#         read = csv.reader(csvfile)
#         for i in read:
#             print(i)
