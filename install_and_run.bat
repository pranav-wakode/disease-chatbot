@echo off
echo ========================================
echo AI Health & Wellness Assistant
echo ========================================
echo.
echo This script will install dependencies and run the application
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found. Checking version...
python --version

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
for /f "tokens=2 delims=." %%a in ("%PYTHON_VERSION%") do set PYTHON_MAJOR=%%a
for /f "tokens=3 delims=." %%b in ("%PYTHON_VERSION%") do set PYTHON_MINOR=%%b

if %PYTHON_MAJOR% LSS 3 (
    echo ERROR: Python 3.8 or higher is required
    echo Current version: %PYTHON_VERSION%
    pause
    exit /b 1
)

if %PYTHON_MAJOR%==3 if %PYTHON_MINOR% LSS 8 (
    echo ERROR: Python 3.8 or higher is required
    echo Current version: %PYTHON_VERSION%
    pause
    exit /b 1
)

echo Python version check passed.
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo Installing dependencies...
echo This may take several minutes on first run...
echo.

REM Install dependencies
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo WARNING: Some dependencies failed to install
    echo Trying alternative installation methods...
    echo.
    
    REM Try pipwin for PyAudio
    pip install pipwin
    pipwin install pyaudio
    
    REM Try installing remaining packages
    pip install transformers torch torchaudio SpeechRecognition gTTS pygame pillow numpy
)

echo.
echo Dependencies installation completed.
echo.

REM Test installation
echo Testing installation...
python test_installation.py

if errorlevel 1 (
    echo.
    echo WARNING: Some modules failed to import
    echo You may need to install additional system dependencies
    echo.
)

echo.
echo ========================================
echo Installation completed!
echo ========================================
echo.
echo Starting the Health Assistant...
echo.
echo IMPORTANT SAFETY REMINDER:
echo - This is NOT a medical device
echo - Always consult healthcare professionals for medical advice
echo - The AI provides general information only
echo.
echo Press any key to continue...
pause >nul

REM Run the application
python main.py

echo.
echo Application closed.
pause
