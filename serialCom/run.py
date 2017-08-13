#!/usr/bin/env python3

import os
import subprocess
import sys

appdir = os.path.abspath("serialcom/main.py")
print(appdir)
def run():
    assert os.path.exists(appdir)
    os.environ["APP_DIR"] = appdir

    subprocess.call([sys.executable, appdir])

run()