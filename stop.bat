@echo off
setlocal EnableDelayedExpansion

REM ============================================================
REM  Plants vs Zombies - Windows Stop Script (stop.bat)
REM  Feature: Find and terminate game processes
REM  Usage: stop.bat [options]
REM    --force / -f    Force kill (terminate immediately)
REM    --help / -h     Show help
REM ============================================================

REM ==================== Logging Config ====================
set "LOG_FILE=%~dp0game_launch.log"
set "TIMESTAMP=%date:~0,4%-%date:~5,2%-%date:~8,2% %time:~0,8%"
echo [%TIMESTAMP%] [INFO] Stop script started >> "%LOG_FILE%"

REM ==================== Help Option ====================
if "%~1"=="--help" goto :show_help
if "%~1"=="-h" goto :show_help

REM ==================== Parse Args ====================
set "FORCE_KILL=0"
if "%~1"=="--force" set "FORCE_KILL=1"
if "%~1"=="-f" set "FORCE_KILL=1"

REM ==================== Python Check ====================
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    call :log ERROR "Python not found, cannot search for processes"
    echo [ERROR] Python not found in PATH.
    echo         Please install Python or use Task Manager manually.
    goto :error_exit
)

REM ==================== Header ====================
echo.
echo ============================================================
echo   Plants vs Zombies - Stop Game
echo ============================================================
echo.

call :log INFO "Searching for game processes..."

REM ==================== Check psutil availability ====================
python -c "import psutil" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    call :log WARN "psutil not installed, attempting auto-install..."
    echo [WARN] psutil library not found. Installing for better process detection...
    python -m pip install psutil >nul 2>&1
    if !ERRORLEVEL! neq 0 (
        call :log WARN "psutil install failed, using basic process detection"
        echo [WARN] psutil install failed. Using basic detection mode.
        goto :basic_detection
    )
    call :log INFO "psutil installed successfully"
    echo [INFO] psutil installed.
)

REM ==================== Find Game Processes via psutil ====================
set "PROCESS_LIST="
set "FOUND=0"

for /f "delims=" %%i in (
    'python -c "import psutil; [print(p.pid) for p in psutil.process_iter([\"pid\",\"cmdline\"]) if p.info[\"cmdline\"] and \"main.py\" in \" \".join(p.info[\"cmdline\"])]" 2^>nul'
) do (
    if not "%%i"=="" (
        set "FOUND=1"
        set "PROCESS_LIST=!PROCESS_LIST! %%i"
        call :log INFO "Found game process PID: %%i"
    )
)

if %FOUND% equ 0 goto :no_processes
goto :terminate

REM ==================== Basic Detection Fallback ====================
:basic_detection
call :log INFO "Using basic process detection (tasklist)"
set "PROCESS_LIST="
set "FOUND=0"

REM List all python.exe processes
echo [INFO] Basic detection mode - listing Python processes:
echo.
echo   PID       Process Name
echo   --------  -------------------
for /f "skip=3 tokens=1,2 delims= " %%a in (
    'tasklist /fi "imagename eq python.exe" /fo table /nh 2^>nul'
) do (
    if not "%%b"=="" (
        echo   %%b       %%a
        set "FOUND=1"
        set "PROCESS_LIST=!PROCESS_LIST! %%b"
        call :log INFO "Python process found PID: %%b (basic detection)"
    )
)
for /f "skip=3 tokens=1,2 delims= " %%a in (
    'tasklist /fi "imagename eq pythonw.exe" /fo table /nh 2^>nul'
) do (
    if not "%%b"=="" (
        echo   %%b       %%a
        set "FOUND=1"
        set "PROCESS_LIST=!PROCESS_LIST! %%b"
        call :log INFO "Python process found PID: %%b (basic detection)"
    )
)

if %FOUND% equ 0 goto :no_processes

echo.
echo [WARN] In basic detection mode, ALL Python processes will be terminated.
echo        To stop only the game, install psutil: pip install psutil
set /p CONFIRM="Continue? (y/N): "
if /i not "!CONFIRM!"=="y" (
    call :log INFO "User cancelled operation"
    echo [INFO] Operation cancelled.
    goto :end
)
goto :terminate

REM ==================== No Processes Found ====================
:no_processes
call :log INFO "No game processes found"
echo [INFO] No game processes found running.
echo.
echo        If you believe the game is running, try:
echo        1. Install psutil: pip install psutil
echo        2. Or use Task Manager to end "python.exe" processes
goto :end

REM ==================== Terminate Processes ====================
:terminate
echo.
echo Found %FOUND% game process(es):
for %%p in (%PROCESS_LIST%) do (
    echo   - PID %%p
)
echo.

if %FORCE_KILL% equ 1 (
    call :log INFO "Force killing game processes..."
    echo [INFO] Force killing game processes...
    for %%p in (%PROCESS_LIST%) do (
        taskkill /F /PID %%p >nul 2>&1
        if !ERRORLEVEL! equ 0 (
            call :log INFO "Successfully killed PID %%p"
            echo   [OK] Killed PID %%p
        ) else (
            call :log ERROR "Failed to kill PID %%p"
            echo   [FAIL] Failed to kill PID %%p
        )
    )
) else (
    call :log INFO "Gracefully terminating game processes..."
    echo [INFO] Terminating game processes...
    for %%p in (%PROCESS_LIST%) do (
        taskkill /PID %%p >nul 2>&1
        if !ERRORLEVEL! equ 0 (
            call :log INFO "Successfully terminated PID %%p"
            echo   [OK] Terminated PID %%p
        ) else (
            call :log ERROR "Failed to terminate PID %%p, try --force"
            echo   [FAIL] Failed to terminate PID %%p
            echo          Use --force or -f to force kill
        )
    )
)

echo.
call :log INFO "Stop operation completed"
echo ============================================================
echo   Stop operation completed
echo ============================================================
goto :end

REM ==================== Help ====================
:show_help
echo.
echo ============================================================
echo   Plants vs Zombies - Stop Script Help
echo ============================================================
echo.
echo Usage: stop.bat [options]
echo.
echo Options:
echo   --force / -f    Force kill processes immediately
echo                   (uses taskkill /F)
echo   --help / -h     Show this help
echo.
echo Examples:
echo   stop.bat              Gracefully stop game
echo   stop.bat --force      Force kill game processes
echo   stop.bat -f           Same as above
echo.
echo Notes:
echo   - For best results, install psutil: pip install psutil
echo   - If graceful termination fails, use --force
echo   - All processes running 'python main.py' will be stopped
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
call :log ERROR "Stop script failed"
echo.
echo Troubleshooting:
echo   1. Ensure Python is installed and in PATH
echo   2. Install psutil for better process detection: pip install psutil
echo   3. Check log file: %LOG_FILE%
echo.
endlocal
exit /b 1

REM ==================== Exit ====================
:end
set "TIMESTAMP=%date:~0,4%-%date:~5,2%-%date:~8,2% %time:~0,8%"
echo [%TIMESTAMP%] [INFO] Stop script finished >> "%LOG_FILE%"
endlocal
exit /b 0
