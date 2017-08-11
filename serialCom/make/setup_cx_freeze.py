#! usr/bin/python3
# -*- coding:utf-8 -*-
import os
import sys
from cx_Freeze import setup, Executable

base = None

if sys.platform == "win32":
    base = "Win32GUI"


setup(name="valueReader",
      version="1.0",
      description="value Reader",
      executables=[Executable("valueReader.py", base=base)])
