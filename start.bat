@echo off
echo ========================================
echo AI Automated Red Team Agent (AARTA)
echo ========================================
echo.
echo Starting AARTA Web Interface...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if needed
echo Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo Dependencies installed.
    echo.
)

REM Start the server
echo.
echo ========================================
echo AARTA is starting...
echo ========================================
echo.
echo Frontend URL: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app/main.py
