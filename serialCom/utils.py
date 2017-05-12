# -*- coding:utf-8 -*-
import os
import csv
import time
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


class RotatingFileOpener():
    def __init__(self, path, mode='a', prepend="", append=""):
        if not os.path.isdir(path):
            raise FileNotFoundError(
                "Can't open directory '{}' for data output.".format(path))
        self._path = path
        self._prepend = prepend
        self._append = append
        self._mode = mode
        self._day = time.localtime().tm_mday

    def __enter__(self):
        self._filename = self._format_filename()
        self._file = open(file=self._filename, mode=self._mode,
                          encoding="utf-8", newline="")
        return self

    def __exit__(self, *args):
        return getattr(self._file, '__exit__')(*args)

    def _day_changed(self):
        return self._day != time.localtime().tm_mday

    def _format_filename(self):
        return os.path.join(self._path, "{}{}{}".format(self._prepend, time.strftime("%Y%m%d"), self._append))

    def write(self, *args):
        if self._day_changed():
            self._file.close()
            self._file = open(self._format_filename())
        return getattr(self._file, 'write')(*args)

    def __getattr__(self, attr):
        return getattr(self._file, attr)

    def __iter__(self):
        return iter(self._file)


def hasHeader(filename, header):
    with open(filename, encoding="utf-8", newline="") as csv_file:
        readers = csv.reader(csv_file)
        for row_index, row in enumerate(readers):
            if row_index == 0:
                for i in range(len(header)):
                    if row[i] == header[i]:
                        continue
                    else:
                        return False
                return True
        return False


# 保存到csv文件,csv 文件可以直接用excel打开
def saveCSV(data):
    with RotatingFileOpener(os.path.abspath("."), prepend="valReader-", append=".csv") as csv_file:
        header = ["[Flag Bit]", "[Tight Torque]",
                  "[Tight Angle]", "[Date Time]"]
        writer = csv.writer(csv_file, dialect=("excel"))
        if not hasHeader(csv_file._filename, header):
            writer.writerow(header)
        writer.writerow(data)
