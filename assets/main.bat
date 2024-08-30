@echo off
title Ai-Chat Setup
color a

echo Ai-Chat By Hillorius
echo Requirement: Python
echo.

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

echo Installing required packages...
color a
pip install requests >nul 2>&1
cls

color f
echo Installation complete.
echo Running Ai-Chat...
echo.

python assets/run.py

exit /b
