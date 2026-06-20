@echo off
setlocal EnableDelayedExpansion

REM ============================================================
REM  Plants vs Zombies - Windows Launcher (start.bat)
REM  Feature: env check, dependency validation, error handling, logging
REM  Usage: start.bat [options]
REM    --fullscreen / -f     Launch in fullscreen mode
REM    --fps <value>         Set target FPS (default: 60)
REM    --width <value>       Set window width (default: 900)
REM    --height <value>      Set window height (default: 600)
REM    --bgm-volume <value>  Set BGM volume 0.0-1.0 (default: 0.5)
REM    --sfx-volume <value>  Set SFX volume 0.0-1.0 (default: 0.7)
REM    --no-audio            Disable all audio
REM    --debug               Enable debug mode
REM    --help / -h           Show help
REM ============================================================

REM ==================== Logging Config ====================
set "LOG_FILE=%~dp0game_launch.log"
set "TIMESTAMP=%date:~0,4%-%date:~5,2%-%date:~8,2% %time:~0,8%"
echo [%TIMESTAMP%] [INFO] Launch script started >> "%LOG_FILE%"

REM ==================== Help Option ====================
if "%~1"=="--help" goto :show_help
if "%~1"=="-h" goto :show_help

REM ==================== Working Directory ====================
cd /d "%~dp0"
call :log INFO "Working directory: %CD%"

REM ==================== Python Environment Check ====================
call :log INFO "Checking Python environment..."

python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    call :log ERROR "Python not found. Please install Python and add to PATH."
    echo [ERROR] Python not found. Install Python 3.8+ and add to PATH.
    echo Download: https://www.python.org/downloads/
    goto :error_exit
)

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set "PYTHON_VER=%%v"
call :log INFO "Python version detected: %PYTHON_VER%"

python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    call :log ERROR "Python version too old: %PYTHON_VER%, need 3.8+"
    echo [ERROR] Python version too old: %PYTHON_VER%, need 3.8+
    goto :error_exit
)
call :log INFO "Python version check passed"

REM ==================== Project File Check ====================
call :log INFO "Checking project files..."

if not exist "%~dp0main.py" (
    call :log ERROR "Missing main entry file: main.py"
    echo [ERROR] Missing main.py
    goto :error_exit
)
call :log INFO "File check passed: main.py"

if not exist "%~dp0requirements.txt" (
    call :log WARN "Missing requirements.txt, skipping dependency version check"
    echo [WARN] Missing requirements.txt
) else (
    call :log INFO "File check passed: requirements.txt"
)

if not exist "%~dp0game_core" (
    call :log ERROR "Missing directory: game_core/"
    echo [ERROR] Missing game_core/
    goto :error_exit
)
call :log INFO "Directory check passed: game_core/"

if not exist "%~dp0res" (
    call :log ERROR "Missing directory: res/"
    echo [ERROR] Missing res/
    goto :error_exit
)
call :log INFO "Directory check passed: res/"

if not exist "%~dp0scene" (
    call :log ERROR "Missing directory: scene/"
    echo [ERROR] Missing scene/
    goto :error_exit
)
call :log INFO "Directory check passed: scene/"

if not exist "%~dp0sprites" (
    call :log ERROR "Missing directory: sprites/"
    echo [ERROR] Missing sprites/
    goto :error_exit
)
call :log INFO "Directory check passed: sprites/"

REM ==================== Dependency Check ====================
call :log INFO "Checking dependencies..."

if exist "%~dp0requirements.txt" (
    call :log INFO "Checking dependencies from requirements.txt..."
    python -c "import pygame" >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        call :log WARN "pygame not found, attempting auto-install..."
        echo [WARN] Installing pygame...
        python -m pip install -r "%~dp0requirements.txt"
        if %ERRORLEVEL% neq 0 (
            call :log ERROR "Dependency install failed"
            echo [ERROR] Install failed. Run manually: pip install -r requirements.txt
            goto :error_exit
        )
        call :log INFO "Dependencies installed successfully"
        echo [INFO] Dependencies installed
    ) else (
        call :log INFO "pygame check passed"
    )
) else (
    python -c "import pygame" >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        call :log WARN "pygame not found, attempting auto-install..."
        echo [WARN] Installing pygame...
        python -m pip install "pygame>=2.0.0"
        if %ERRORLEVEL% neq 0 (
            call :log ERROR "pygame install failed"
            echo [ERROR] Install failed. Run manually: pip install pygame
            goto :error_exit
        )
        call :log INFO "pygame installed"
    )
)

REM ==================== Virtual Env Check ====================
call :log INFO "Checking virtual environment..."

python -c "import sys; exit(0 if sys.prefix != sys.base_prefix else 1)" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    call :log INFO "Virtual environment detected"
) else (
    call :log WARN "No virtual environment detected"
    echo [WARN] No virtual environment detected.
    echo   Recommended:
    echo     python -m venv venv
    echo     venv\Scripts\activate
    echo     pip install -r requirements.txt
)

REM ==================== Build Launch Args ====================
call :log INFO "Building launch arguments..."

set "LAUNCH_ARGS="

:parse_args
if "%~1"=="" goto :args_done
set "ARG=%~1"

if "%ARG%"=="--fullscreen" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --fullscreen"
    call :log INFO "Arg: fullscreen mode"
) else if "%ARG%"=="-f" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --fullscreen"
    call :log INFO "Arg: fullscreen mode"
) else if "%ARG%"=="--fps" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --fps %~2"
    call :log INFO "Arg: FPS=%~2"
    shift
) else if "%ARG%"=="--width" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --width %~2"
    call :log INFO "Arg: width=%~2"
    shift
) else if "%ARG%"=="--height" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --height %~2"
    call :log INFO "Arg: height=%~2"
    shift
) else if "%ARG%"=="--bgm-volume" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --bgm-volume %~2"
    call :log INFO "Arg: BGM volume=%~2"
    shift
) else if "%ARG%"=="--sfx-volume" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --sfx-volume %~2"
    call :log INFO "Arg: SFX volume=%~2"
    shift
) else if "%ARG%"=="--no-audio" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --no-audio"
    call :log INFO "Arg: audio disabled"
) else if "%ARG%"=="--debug" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --debug"
    call :log INFO "Arg: debug mode"
) else (
    call :log WARN "Unknown arg: %ARG%"
    echo [WARN] Unknown arg: %ARG%
    set "LAUNCH_ARGS=%LAUNCH_ARGS% %ARG%"
)

shift
goto :parse_args

:args_done

REM ==================== Launch Game ====================
call :log INFO "Launching game..."
call :log INFO "Command: python main.py%LAUNCH_ARGS%"
echo.
echo ============================================================
echo   Plants vs Zombies - Launching...
echo ============================================================
echo.

python "%~dp0main.py"%LAUNCH_ARGS%

if %ERRORLEVEL% neq 0 (
    call :log ERROR "Game exited abnormally (code: %ERRORLEVEL%)"
    echo.
    echo [ERROR] Game exited abnormally (code: %ERRORLEVEL%)
    echo   Check log: %LOG_FILE%
    echo   Use --debug for more info
    goto :error_exit
)

call :log INFO "Game exited normally"
echo.
echo ============================================================
echo   Game exited
echo ============================================================
goto :end

REM ==================== Help ====================
:show_help
echo.
echo ============================================================
echo   Plants vs Zombies - Launcher Help
echo ============================================================
echo.
echo Usage: start.bat [options]
echo.
echo Options:
echo   --fullscreen / -f     Launch in fullscreen
echo   --fps ^<value^>         Target FPS (default: 60)
echo   --width ^<value^>       Window width (default: 900)
echo   --height ^<value^>      Window height (default: 600)
echo   --bgm-volume ^<value^>  BGM volume 0.0-1.0 (default: 0.5)
echo   --sfx-volume ^<value^>  SFX volume 0.0-1.0 (default: 0.7)
echo   --no-audio            Disable audio
echo   --debug               Enable debug logging
echo   --help / -h           Show this help
echo.
echo Examples:
echo   start.bat                        Default config
echo   start.bat --fullscreen           Fullscreen mode
echo   start.bat --fps 30 --no-audio    30 FPS, no audio
echo   start.bat --width 1280 --height 720 --debug
echo                                    Custom resolution + debug
echo.
goto :end

REM ==================== Log Function ====================
:log
set "LOG_LEVEL=%~1"
set "LOG_MSG=%~2"
set "TIMESTAMP=%date:~0,4%-%date:~5,2%-%date:~8,2% %time:~0,8%"
echo [%TIMESTAMP%] [%LOG_LEVEL%] %LOG_MSG% >> "%LOG_FILE%"
if "%LOG_LEVEL%"=="ERROR" (
    echo [ERROR] %LOG_MSG%
) else if "%LOG_LEVEL%"=="WARN" (
    echo [WARN] %LOG_MSG%
)
goto :eof

REM ==================== Error Exit ====================
:error_exit
call :log ERROR "Launch script failed"
echo.
echo Troubleshooting:
echo   1. Check Python 3.8+ : python --version
echo   2. Install deps     : pip install -r requirements.txt
echo   3. Verify files exist
echo   4. Use --debug for more info
echo   5. Check log file  : %LOG_FILE%
echo.
endlocal
exit /b 1

REM ==================== Normal Exit ====================
:end
set "TIMESTAMP=%date:~0,4%-%date:~5,2%-%date:~8,2% %time:~0,8%"
echo [%TIMESTAMP%] [INFO] Launch script finished >> "%LOG_FILE%"
endlocal
exit /b 0
