@echo off

set pwd=%cd%
set nsis=%cd%\..\..\GNSIS
set path=%nsis%;%path%

python %nsis%\make.py release

pause