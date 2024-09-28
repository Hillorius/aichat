@echo off
:: Set title and color
title Ai-Chat By Hillorius
color a

:: Clear screen and display loading animation
cls
echo Loading.
ping localhost -n 2 >nul
cls
echo Loading..
ping localhost -n 2 >nul
cls
echo Loading...
ping localhost -n 2 >nul
cls

:: Install required packages
echo Installing required packages...
color a
pip install requests >nul 2>&1
cls

:: Notify completion
color f
echo Installation complete.
echo Running Ai-Chat...
echo.

:: Run the Python script
python assets/run.py

:: End of script
exit /b
