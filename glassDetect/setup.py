from distutils.core import setup
import py2exe
import sys

#this allows to run it with a simple double click.
sys.argv.append('py2exe')

py2exe_options = {
    "compressed":1,
    "optimize":2,
    "ascii":0,
    "bundle_files":0,
}

setup(name='glassDetect',
      version='1.0',
      console=[{'script':'main.py'}],
      zipfile=None,
      options={'py2exe':py2exe_options})

