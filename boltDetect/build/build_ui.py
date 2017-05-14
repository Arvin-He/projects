# -*- coding:utf-8 -*-

import os
import subprocess
import sys

inputFile = os.path.abspath(os.path.join("../res", "boltdetect.ui"))
print(inputFile)
outputFile = os.path.abspath("../boltdetect_ui.py")
print(outputFile)
subprocess.call(["pyuic5.bat", inputFile, "-o", outputFile])

# pyqtuic5.exe boltdetect.ui -o ../boltdetect_ui.py