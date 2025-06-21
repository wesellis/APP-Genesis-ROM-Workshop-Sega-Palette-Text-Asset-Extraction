@echo off
REM Genesis ROM Workshop Launcher
REM Professional tools for real ROM modification

echo ========================================
echo   Genesis ROM Workshop v1.0
echo   Professional ROM Modification Tools
echo ========================================
echo.
echo What this workshop can do:
echo   * Palette modification (95%% success)
echo   * Text extraction/replacement
echo   * Asset extraction  
echo   * ROM analysis
echo.
echo What it cannot do:
echo   * 60fps enhancement (impossible)
echo   * Widescreen conversion (impossible)
echo   * HD scaling (emulator feature)
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Check if main script exists
if not exist "grw_pipeline.py" (
    echo ❌ grw_pipeline.py not found
    echo Make sure you're running this from the project directory
    pause
    exit /b 1
)

echo Starting Genesis ROM Workshop...
echo.
python grw_pipeline.py

pause
