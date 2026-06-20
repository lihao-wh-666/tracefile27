@echo off
chcp 65001 >nul 2>&1
setlocal EnableDelayedExpansion

REM ============================================================
REM 植物大战僵尸 - Windows 启动脚本
REM 功能: 环境检测、依赖验证、参数解析、日志记录、游戏启动
REM 用法: start.bat [选项]
REM   --fullscreen / -f     以全屏模式启动
REM   --fps <数值>          设置目标帧率 (默认: 60)
REM   --width <数值>        设置窗口宽度 (默认: 900)
REM   --height <数值>       设置窗口高度 (默认: 600)
REM   --bgm-volume <数值>   设置背景音乐音量 0.0-1.0 (默认: 0.5)
REM   --sfx-volume <数值>   设置音效音量 0.0-1.0 (默认: 0.7)
REM   --no-audio            禁用所有音频
REM   --debug               启用调试模式
REM   --help / -h           显示帮助信息
REM ============================================================

REM ==================== 日志配置 ====================
set "LOG_FILE=%~dp0game_launch.log"
set "TIMESTAMP="

call :get_timestamp
echo [%TIMESTAMP%] [INFO] 启动脚本开始执行 >> "%LOG_FILE%"

REM ==================== 显示帮助信息 ====================
if "%~1"=="--help" goto :show_help
if "%~1"=="-h" goto :show_help

REM ==================== 工作目录设置 ====================
cd /d "%~dp0"
call :log INFO "工作目录: %CD%"

REM ==================== Python 环境检测 ====================
call :log INFO "正在检测 Python 环境..."

where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    call :log ERROR "未找到 Python，请确保 Python 已安装并添加到系统 PATH"
    echo [错误] 未找到 Python，请安装 Python 3.8+ 并添加到 PATH
    echo 下载地址: https://www.python.org/downloads/
    goto :error_exit
)

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set "PYTHON_VER=%%v"
call :log INFO "检测到 Python 版本: %PYTHON_VER%"

python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    call :log ERROR "Python 版本过低: %PYTHON_VER%，需要 3.8 或更高版本"
    echo [错误] Python 版本过低，请升级到 Python 3.8+
    goto :error_exit
)
call :log INFO "Python 版本检查通过"

REM ==================== 项目文件完整性检查 ====================
call :log INFO "正在检查项目文件完整性..."

if not exist "%~dp0main.py" (
    call :log ERROR "缺少主入口文件: main.py"
    echo [错误] 缺少主入口文件: main.py
    goto :error_exit
)
call :log INFO "主入口文件检查通过: main.py"

if not exist "%~dp0requirements.txt" (
    call :log WARN "缺少依赖清单文件: requirements.txt"
    echo [警告] 缺少 requirements.txt，跳过依赖版本验证
) else (
    call :log INFO "依赖清单文件检查通过: requirements.txt"
)

if not exist "%~dp0game_core" (
    call :log ERROR "缺少核心模块目录: game_core/"
    echo [错误] 缺少核心模块目录: game_core/
    goto :error_exit
)
call :log INFO "核心模块目录检查通过: game_core/"

if not exist "%~dp0res" (
    call :log ERROR "缺少资源模块目录: res/"
    echo [错误] 缺少资源模块目录: res/
    goto :error_exit
)
call :log INFO "资源模块目录检查通过: res/"

if not exist "%~dp0scene" (
    call :log ERROR "缺少场景模块目录: scene/"
    echo [错误] 缺少场景模块目录: scene/
    goto :error_exit
)
call :log INFO "场景模块目录检查通过: scene/"

if not exist "%~dp0sprites" (
    call :log ERROR "缺少精灵模块目录: sprites/"
    echo [错误] 缺少精灵模块目录: sprites/
    goto :error_exit
)
call :log INFO "精灵模块目录检查通过: sprites/"

REM ==================== 依赖库验证 ====================
call :log INFO "正在验证依赖库..."

if exist "%~dp0requirements.txt" (
    call :log INFO "正在检查 requirements.txt 中的依赖..."
    python -c "import pygame; print(pygame.version.ver)" >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        call :log WARN "缺少 pygame 依赖，尝试自动安装..."
        echo [警告] 缺少 pygame 依赖，正在自动安装...
        pip install -r "%~dp0requirements.txt"
        if %ERRORLEVEL% neq 0 (
            call :log ERROR "依赖安装失败"
            echo [错误] 依赖安装失败，请手动运行: pip install -r requirements.txt
            goto :error_exit
        )
        call :log INFO "依赖安装成功"
        echo [信息] 依赖安装成功
    ) else (
        call :log INFO "pygame 依赖检查通过"
    )
) else (
    python -c "import pygame" >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        call :log WARN "缺少 pygame 依赖，尝试自动安装..."
        echo [警告] 缺少 pygame 依赖，正在自动安装...
        pip install pygame>=2.0.0
        if %ERRORLEVEL% neq 0 (
            call :log ERROR "pygame 安装失败"
            echo [错误] pygame 安装失败，请手动运行: pip install pygame
            goto :error_exit
        )
        call :log INFO "pygame 安装成功"
    )
)

REM ==================== 虚拟环境检测 ====================
call :log INFO "正在检测虚拟环境..."

python -c "import sys; print(sys.prefix != sys.base_prefix)" 2>nul | findstr /C:"True" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    call :log INFO "检测到虚拟环境: %VIRTUAL_ENV%"
) else (
    call :log WARN "未检测到虚拟环境，建议使用虚拟环境运行游戏"
    echo [警告] 未检测到虚拟环境
    echo   建议创建虚拟环境:
    echo     python -m venv venv
    echo     venv\Scripts\activate
    echo     pip install -r requirements.txt
)

REM ==================== 构建启动参数 ====================
call :log INFO "正在构建启动参数..."

set "LAUNCH_ARGS="

:parse_args
if "%~1"=="" goto :args_done
set "ARG=%~1"

if "%ARG%"=="--fullscreen" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --fullscreen"
    call :log INFO "参数: 全屏模式"
) else if "%ARG%"=="-f" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --fullscreen"
    call :log INFO "参数: 全屏模式"
) else if "%ARG%"=="--fps" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --fps %~2"
    call :log INFO "参数: 帧率=%~2"
    shift
) else if "%ARG%"=="--width" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --width %~2"
    call :log INFO "参数: 窗口宽度=%~2"
    shift
) else if "%ARG%"=="--height" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --height %~2"
    call :log INFO "参数: 窗口高度=%~2"
    shift
) else if "%ARG%"=="--bgm-volume" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --bgm-volume %~2"
    call :log INFO "参数: BGM音量=%~2"
    shift
) else if "%ARG%"=="--sfx-volume" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --sfx-volume %~2"
    call :log INFO "参数: SFX音量=%~2"
    shift
) else if "%ARG%"=="--no-audio" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --no-audio"
    call :log INFO "参数: 禁用音频"
) else if "%ARG%"=="--debug" (
    set "LAUNCH_ARGS=%LAUNCH_ARGS% --debug"
    call :log INFO "参数: 调试模式"
) else (
    call :log WARN "未知参数: %ARG%"
    echo [警告] 未知参数: %ARG%
    set "LAUNCH_ARGS=%LAUNCH_ARGS% %ARG%"
)

shift
goto :parse_args

:args_done

REM ==================== 启动游戏 ====================
call :log INFO "正在启动游戏..."
call :log INFO "启动命令: python main.py%LAUNCH_ARGS%"
echo.
echo ============================================================
echo   植物大战僵尸 - 正在启动...
echo ============================================================
echo.

python "%~dp0main.py"%LAUNCH_ARGS%

if %ERRORLEVEL% neq 0 (
    call :log ERROR "游戏异常退出，退出码: %ERRORLEVEL%"
    echo.
    echo [错误] 游戏异常退出 (退出码: %ERRORLEVEL%)
    echo   请查看日志文件: %LOG_FILE%
    echo   尝试使用 --debug 参数启动以获取更多信息
    goto :error_exit
)

call :log INFO "游戏正常退出"
echo.
echo ============================================================
echo   游戏已退出
echo ============================================================
goto :end

REM ==================== 帮助信息 ====================
:show_help
echo.
echo ============================================================
echo   植物大战僵尸 - 启动脚本帮助
echo ============================================================
echo.
echo 用法: start.bat [选项]
echo.
echo 启动选项:
echo   --fullscreen / -f     以全屏模式启动游戏
echo   --fps ^<数值^>          设置目标帧率 (默认: 60)
echo   --width ^<数值^>        设置窗口宽度 (默认: 900)
echo   --height ^<数值^>       设置窗口高度 (默认: 600)
echo   --bgm-volume ^<数值^>   设置背景音乐音量 0.0-1.0 (默认: 0.5)
echo   --sfx-volume ^<数值^>   设置音效音量 0.0-1.0 (默认: 0.7)
echo   --no-audio            禁用所有音频
echo   --debug               启用调试模式，输出详细日志
echo   --help / -h           显示此帮助信息
echo.
echo 示例:
echo   start.bat                        以默认配置启动
echo   start.bat --fullscreen           以全屏模式启动
echo   start.bat --fps 30 --no-audio    以30帧率且无音频启动
echo   start.bat --width 1280 --height 720 --debug
echo                                     自定义分辨率+调试模式启动
echo.
goto :end

REM ==================== 日志函数 ====================
:log
set "LOG_LEVEL=%~1"
set "LOG_MSG=%~2"
call :get_timestamp
echo [%TIMESTAMP%] [%LOG_LEVEL%] %LOG_MSG% >> "%LOG_FILE%"
if "%LOG_LEVEL%"=="ERROR" (
    echo [错误] %LOG_MSG%
) else if "%LOG_LEVEL%"=="WARN" (
    echo [警告] %LOG_MSG%
)
goto :eof

:get_timestamp
for /f "tokens=1-6 delims=/ :." %%a in ('wmic os get localdatetime ^| find "."') do (
    set "TIMESTAMP=%%a/%%b/%%c %%d:%%e:%%f"
)
goto :eof

REM ==================== 错误退出 ====================
:error_exit
call :log ERROR "启动脚本执行失败"
echo.
echo 故障排查指南:
echo   1. 确认已安装 Python 3.8+ : python --version
echo   2. 确认已安装依赖: pip install -r requirements.txt
echo   3. 检查项目文件完整性
echo   4. 使用 --debug 参数查看详细日志
echo   5. 查看日志文件: %LOG_FILE%
echo.
endlocal
exit /b 1

REM ==================== 正常退出 ====================
:end
call :get_timestamp
echo [%TIMESTAMP%] [INFO] 启动脚本执行完毕 >> "%LOG_FILE%"
endlocal
exit /b 0
