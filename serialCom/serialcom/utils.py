# -*- coding:utf-8 -*-
import os
import time
import configparser
from operator import itemgetter
from log import logger


# 读配置文件
def read_config(config_path, field, key):
    cf = configparser.ConfigParser()
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cf.read_file(f)
        result = cf.get(field, key)
    except Exception as e:
        logger.info("read_config {} {} {} {}".format(
            config_path, field, key, e))
        return ""
    return result


# 写配置文件
def write_config(config_path, field, key, value):
    cf = configparser.ConfigParser()
    cf.optionxform = str
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cf.read_file(f)
        cf.set(field, key, value)
        cf.write(open(config_path, "w", encoding="utf-8"))
    except Exception as e:
        logger.error(e)
        return False
    return True


# 读txt文件获取barcode
def read_txt(file_path):
    txt_files = os.listdir(file_path)
    barcodes = []
    if len(txt_files) > 2:
        file_info = []
        file_info_by_ctime = []
        for txt in txt_files:
            ctime = os.path.getctime(os.path.join(file_path, txt))
            file_info.append({"txt": txt, "ctime": ctime})
        # for item in reversed(sorted(file_info,  key=itemgetter('ctime'))):
            # barcodes.append(item["txt"])
        file_info_by_ctime = reversed(sorted(file_info,  key=itemgetter('ctime')))
        barcodes.append(file_info_by_ctime[0])
        # print(file_info_by_ctime)
    for txt in txt_files:
        # ctime = time.localtime(os.path.getctime(os.path.join(file_path, txt)))
        # print(ctime)
        # print("{}年{}月{}日 {}时{}分{}秒".format(ctime[0], ctime[1], ctime[2], ctime[3], ctime[4], ctime[5]))
        barcode_info = os.path.splitext(txt)[0].split('_')
        barcodes.append(barcode_info)
    print(barcodes)
        
        # if txt.startswith("barcode1"):
        #     barcode1 = txt.split('_')[1]
        # if txt.startswith("barcode2"):
        #     barcode2 = txt.split('_')[1]
    # pass