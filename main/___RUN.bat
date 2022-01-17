@echo off

:loop
python _force_main_DER_atrSupertrend.py
echo Looped
TIMEOUT /T 20
goto loop