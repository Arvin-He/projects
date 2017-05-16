# -*- coding:utf-8 -*-

import os
import subprocess
import sys

inputFile = os.path.abspath(os.path.join("../res", "glassdetectdlg.ui"))
print("input file ={}".format(inputFile))
outputFile = os.path.abspath("../glassdetectdlg_ui.py")
print("output file ={}".format(outputFile))
subprocess.call(["pyuic5.bat", inputFile, "-o", outputFile])
print("build ui done.")
