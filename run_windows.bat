@echo off
echo Setting up Windows environment for AI Forex Trader...

REM Set UTF-8 encoding for Windows console
chcp 65001 >nul

REM Set environment variables for proper Unicode support
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

echo Starting AI Forex Trading System...
echo.

REM Run the trader
python forex_trader2.py

echo.
echo AI Forex Trading System stopped.
pause