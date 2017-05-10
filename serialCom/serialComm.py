# -*- coding:utf-8 -*-
import os
import csv
import serial
import binascii

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


def closeCom():
    global ser
    if ser.is_open:
        ser.close()
        print("串口已经关闭!")


def writeData():
    global ser
    assert ser.is_open
    # data = "\x53\x07\x01\x01\x04\x30\x02\x64\x45".encode('utf-8')
    # data = bytes([83, 7, 1, 1, 4, 48, 2, 100, 69])
    # 16进制转bytes
    data = bytes.fromhex('53 07 01 01 04 30 02 64 45')
    ser.write(data)


# 读取字节并转换成16进制字符串
def readData():
    global ser
    # assert ser.is_open
    # data = ser.read(13)
    # data = bytes.fromhex('53 0b 01 01 04 30 02 00 00 00 00 c2 45')
    data = bytes.fromhex('53 0b 01 01 04 30 02 b2 4a 58 09 6b 45')
    # 将bytes的内容转16进制表示的bytes
    data2 = binascii.hexlify(data)
    # 将bytes转字符串,并返回
    return data2.decode('utf-8')


# 读到的数据字符串"53 0B  01 01 04 30 02 B2 4A 58 09 6B 45",取其中的第8~11个16进制数
# 然后将取到的16进制数作为一个整体,转换成10进制数,并返回
def transformData(data):
    data.replace(" ", "")
    data2 = data[14:22]
    data3 = reversed([data2[i:i+2] for i in range(0, len(data2), 2)])
    return "".join(data3)


# 将16进制的字符串转换成10进制字符串
def processData(data):
    data2 = str(int(data, 16))
    print(data2)
    return data2


def getFlagBit(data):
    return data[0]


def getTightTorque(data):
    data2 = data[1:5]
    return data2


def getTightAngle(data):
    data2 = data[5:]
    return data2


# 保存到csv文件,csv文件可以导入到excel中去
def saveCSV(data):
    try:
        with open("serialdata.csv", "a", newline="", encoding="utf-8") as csv_file:
            # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
            writer = csv.writer(csv_file, dialect=("excel"))
            # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
            head = ["序号", "标志位", "力矩", "角度"]
            if head is not None:
                writer.writerow(head)
            for row in data:
                writer.writerow(row)
            print("Write a CSV file to path %s Successful." % "path") 
            # csvwriter.writerow(["序号", "标志位", "力矩", "角度"])
    except Exception as e:
        print("Write an CSV file to path: %s, Case: %s" % ("path", e))


# 读取csv文件
def readCSV():
    with open("serialdata.csv", "r", encoding="utf-8") as csv_file:
        # 读取csv文件，返回的是迭代类型
        read = csv.reader(csv_file)
        for i in read:
            print(i)
