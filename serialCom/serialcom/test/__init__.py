import sys

from os.path import dirname, abspath, join, sep

serialcom = dirname(dirname(abspath(__file__)))
print(serialcom)

sys.path.insert(0, serialcom)