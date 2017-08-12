#! usr/bin/python3
# -*- coding:utf-8 -*-
import os
import sys
from cx_Freeze import setup, Executable


local_files = []
if os.path.exists("log/"):
    local_files.append("log/")
elif os.path.exists("userdata/"):
    local_files.append("userdata/")
elif os.path.exists("config/"):
    local_files.append("config/")


# 依赖会自动检测,但会需要微调
build_exe_options = {
    "packages": ["sqlalchemy"],
    "excludes": ["tkinter"],
    "includes": [],
    "include_files": local_files,
}

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('main.py', targetName="valueReader.exe", base=base)
]


setup(
    name="valueReader",
    version="1.0",
    description="A PyQt Value Reader Program",
    options={"build_exe": build_exe_options},
    executables=executables
)
