# -*- coding:utf-8 -*-

import os
import subprocess
import sys

inputFile = os.path.abspath(os.path.join("../res", "serialCom.ui"))
print("input file ={}".format(inputFile))
outputFile = os.path.abspath("../serialCom_ui.py")
print("output file ={}".format(outputFile))
# py3.4.3
try:
    subprocess.call(["pyuic5.bat", inputFile, "-o", outputFile])
except:
# py3.6
    subprocess.call(["pyuic5", inputFile, "-o", outputFile])
print("build ui done.")
