@echo off

:loop
python _atrSupertrend_run.py
echo Looped
TIMEOUT /T 20
goto loop