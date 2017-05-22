#! usr/bin/python3
# -*- coding:utf-8 -*-

import sys

from cx_Freeze import setup, Executable

base = None

if sys.platform == "win32":
    base = "Win32GUI"


setup(name="boltDetect",
      version="1.0",
      description="detect bolts",
      executables=[Executable("run.py", base=base)])
