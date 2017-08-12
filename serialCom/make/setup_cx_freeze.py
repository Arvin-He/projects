# -*- coding:utf-8 -*-
import sys
from cx_Freeze import setup, Executable

# 依赖会自动检测,但会需要微调
build_exe_options = {
    "packages": ["sqlalchemy"],
    "excludes": ["tkinter"],
    "includes": [],
    "include_files": []
}

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('valueReader.py', base=base)
]


setup(
    name="valueReader",
    version="1.0",
    description="A PyQt Value Reader Program",
    options={"build_exe": build_exe_options},
    executables=executables
)
