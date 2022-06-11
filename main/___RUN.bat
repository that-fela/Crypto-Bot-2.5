@echo off

:loop
python _ema3ema6ema9_run.py
echo Looped
TIMEOUT /T 20
goto loop