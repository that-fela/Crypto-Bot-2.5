@echo off

:loop
python _force_main_DER.py
TIMEOUT /T 20
goto loop