# -*- coding:utf-8 -*-
import os
import configparser
from logger import logger


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


# # 获取图像路径
def getImageList(image_path):
    image_list = []
    for img in os.listdir(image_path):
        if img.endswith(".bmp") or img.endswith(".png"):
            image_list.append(os.path.normpath(os.path.join(image_path, img)))
    return image_list
