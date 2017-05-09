# -*- coding:utf-8 -*-
import os
import configparser


# 读配置文件
def read_config(config_path, field, key):
    cf = configparser.ConfigParser()
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cf.read_file(f)
        result = cf.get(field, key)
    except Exception as e:
        print("read_config", config_path, field, key, e)
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
        print(e)
        return False
    return True