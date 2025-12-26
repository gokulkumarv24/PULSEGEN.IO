@echo off
REM Setup script for Module Extraction AI Agent
REM This script installs dependencies and sets up the environment

echo ================================
echo Module Extraction AI Agent Setup
echo ================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Dependencies installed successfully!
    echo.
    echo Quick Start:
    echo 1. Command Line: python module_extractor.py --urls https://help.example.com
    echo 2. Web Interface: streamlit run streamlit_app.py
    echo.
    echo For detailed instructions, see README.md
) else (
    echo.
    echo ❌ Installation failed. Please check your Python environment.
)

pause