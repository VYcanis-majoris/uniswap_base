@echo off
REM Check for dependencies installation
echo Checking for dependencies installation...
pip install -r requirements.txt
echo Dependencies installed successfully.

REM Prompt user for token_send and token_receive addresses
set /p token_send=Enter the token_send address:
set /p token_receive=Enter the token_receive address:

REM Write token_send and token_receive to config.ini file
powershell -Command "(Get-Content 'config.ini') -replace 'token_send = .*', 'token_send = %token_send%' | Set-Content 'config.ini'"
powershell -Command "(Get-Content 'config.ini') -replace 'token_receive = .*', 'token_receive = %token_receive%' | Set-Content 'config.ini'"

REM Run Python script
echo Running main.py...
python main.py
