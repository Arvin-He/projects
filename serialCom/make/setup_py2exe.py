from distutils.core import setup
import py2exe

setup(windows=['valueReader.py'], options={"py2exe": {"includes": ["sip"]}})
