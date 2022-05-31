@ECHO OFF
if not "%1" == "max" start /MAX cmd /c %0 max & exit/b
ECHO Starting...
color 0A
:: start cmd.exe
ECHO Click enter
PAUSE
tree C: /F
PAUSE
