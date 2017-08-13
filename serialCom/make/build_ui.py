# -*- coding:utf-8 -*-
import os
import sys
import subprocess


inputFile = os.path.abspath(os.path.join("../serialcom/res", "serialcom.ui"))
print("input file ={}".format(inputFile))
outputFile = os.path.abspath("../serialcom/serialcom_ui.py")
print("output file ={}".format(outputFile))
try:
    # py3.4.3
    subprocess.call(["pyuic5.bat", inputFile, "-o", outputFile])
except:
    # py3.6
    subprocess.call(["pyuic5", inputFile, "-o", outputFile])
print("build ui done.")
