# -*- coding:utf-8 -*-
from distutils.core import setup
import py2exe

setup(windows=['valueReader.py'], options={"py2exe": {"includes": ["sip"]}})

# 使用py2exe打包时,pyqt的下platform文件夹不会被打包,需要手动拷贝
