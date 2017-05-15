# -*- coding:utf-8 -*-

import os
import subprocess
import sys

inputFile = os.path.abspath(os.path.join("../res", "glassdetectdlg.ui"))
outputFile = os.path.abspath("../glassdetectdlg_ui.py")
subprocess.call(["pyuic5.bat", inputFile, "-o", outputFile])

