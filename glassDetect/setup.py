from distutils.core import setup
import py2exe
# import sys

# this allows to run it with a simple double click.
# sys.argv.append('py2exe')

# py2exe_options = {
#     "compressed": 1,
#     "optimize": 2,
#     "ascii": 0,
#     "bundle_files": 0,
#     "includes": ["sip"]
# }

# setup(name='glassDetect',
#       version='1.0',
#       windows=[{'script': 'run.py'}],
#       zipfile=None,
#       options={'py2exe': py2exe_options})

# setup(windows=['glassDetect.py'], options={"py2exe": {"includes": ["sip"]}})

setup(windows=['run.py'], options={"py2exe": {"includes": ["sip"]}})
# setup(windows=['glassdetectdlg.py'], options={"py2exe": {"includes": ["sip"]}})