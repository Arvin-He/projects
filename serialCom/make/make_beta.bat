@echo off

set pwd=%cd%
set nsis=%cd%\..\..\GNSIS
set path=%nsis%;%path%

python %nsis%\make.py beta

pause