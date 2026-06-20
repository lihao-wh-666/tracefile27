#!/usr/bin/env bash
# ============================================================
# 植物大战僵尸 - Linux/macOS 启动脚本
# 功能: 环境检测、依赖验证、权限检查、参数解析、日志记录、游戏启动
# 用法: ./start.sh [选项]
#   --fullscreen / -f     以全屏模式启动
#   --fps <数值>          设置目标帧率 (默认: 60)
#   --width <数值>        设置窗口宽度 (默认: 900)
#   --height <数值>       设置窗口高度 (默认: 600)
#   --bgm-volume <数值>   设置背景音乐音量 0.0-1.0 (默认: 0.5)
#   --sfx-volume <数值>   设置音效音量 0.0-1.0 (默认: 0.7)
#   --no-audio            禁用所有音频
#   --debug               启用调试模式
#   --help / -h           显示帮助信息
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/game_launch.log"

# ==================== 日志函数 ====================
# 用法: log LEVEL "消息"
# 日志同时输出到终端（ERROR/WARN级别）和日志文件
log() {
    local level="$1"
    shift
    local msg="$*"
    local timestamp
    timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    local entry="[${timestamp}] [${level}] ${msg}"
    echo "${entry}" >> "${LOG_FILE}"
    case "${level}" in
        ERROR) echo "[错误] ${msg}" ;;
        WARN)  echo "[警告] ${msg}" ;;
    esac
}

# ==================== 显示帮助信息 ====================
show_help() {
    cat <<EOF

============================================================
  植物大战僵尸 - 启动脚本帮助
============================================================

用法: ./start.sh [选项]

启动选项:
  --fullscreen / -f     以全屏模式启动游戏
  --fps <数值>          设置目标帧率 (默认: 60)
  --width <数值>        设置窗口宽度 (默认: 900)
  --height <数值>       设置窗口高度 (默认: 600)
  --bgm-volume <数值>   设置背景音乐音量 0.0-1.0 (默认: 0.5)
  --sfx-volume <数值>   设置音效音量 0.0-1.0 (默认: 0.7)
  --no-audio            禁用所有音频
  --debug               启用调试模式，输出详细日志
  --help / -h           显示此帮助信息

示例:
  ./start.sh                        以默认配置启动
  ./start.sh --fullscreen           以全屏模式启动
  ./start.sh --fps 30 --no-audio    以30帧率且无音频启动
  ./start.sh --width 1280 --height 720 --debug
                                     自定义分辨率+调试模式启动
EOF
}

# ==================== 错误退出 ====================
# 用法: error_exit "错误消息"
error_exit() {
    log ERROR "$1"
    echo ""
    echo "故障排查指南:"
    echo "  1. 确认已安装 Python 3.8+ : python3 --version"
    echo "  2. 确认已安装依赖: pip3 install -r requirements.txt"
    echo "  3. 检查项目文件完整性"
    echo "  4. 使用 --debug 参数查看详细日志"
    echo "  5. 查看日志文件: ${LOG_FILE}"
    echo ""
    exit 1
}

# ==================== 脚本启动 ====================
log INFO "启动脚本开始执行"

# 显示帮助信息
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    show_help
    exit 0
fi

# ==================== 工作目录设置 ====================
cd "${SCRIPT_DIR}"
log INFO "工作目录: $(pwd)"

# ==================== 执行权限检查 ====================
log INFO "正在检查脚本执行权限..."

if [[ ! -r "${SCRIPT_DIR}/main.py" ]]; then
    log ERROR "无法读取 main.py，请检查文件权限"
    error_exit "无法读取 main.py，请检查文件权限"
fi

if [[ ! -x "${SCRIPT_DIR}/main.py" ]]; then
    log WARN "main.py 不具有执行权限，尝试修复..."
    chmod +x "${SCRIPT_DIR}/main.py" 2>/dev/null || true
fi

log INFO "文件权限检查通过"

# ==================== Python 环境检测 ====================
log INFO "正在检测 Python 环境..."

PYTHON_CMD=""
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    error_exit "未找到 Python，请安装 Python 3.8+"
fi

PYTHON_VER=$("${PYTHON_CMD}" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')
log INFO "检测到 Python 版本: ${PYTHON_VER} (${PYTHON_CMD})"

"${PYTHON_CMD}" -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"
if [[ $? -ne 0 ]]; then
    error_exit "Python 版本过低: ${PYTHON_VER}，需要 3.8 或更高版本"
fi
log INFO "Python 版本检查通过"

# ==================== 项目文件完整性检查 ====================
log INFO "正在检查项目文件完整性..."

check_path() {
    local path="${SCRIPT_DIR}/$1"
    local desc="$2"
    if [[ ! -e "${path}" ]]; then
        log ERROR "缺少${desc}: ${path}"
        error_exit "缺少${desc}: $1"
    fi
    log INFO "${desc}检查通过: $1"
}

check_path "main.py" "主入口文件"
check_path "requirements.txt" "依赖清单文件"
check_path "game_core" "核心模块目录"
check_path "res" "资源模块目录"
check_path "scene" "场景模块目录"
check_path "sprites" "精灵模块目录"

# ==================== 依赖库验证 ====================
log INFO "正在验证依赖库..."

check_pip_deps() {
    log INFO "正在检查 requirements.txt 中的依赖..."
    if ! "${PYTHON_CMD}" -c "import pygame" &>/dev/null; then
        log WARN "缺少 pygame 依赖，尝试自动安装..."
        echo "[警告] 缺少 pygame 依赖，正在自动安装..."
        "${PYTHON_CMD}" -m pip install -r "${SCRIPT_DIR}/requirements.txt"
        if [[ $? -ne 0 ]]; then
            error_exit "依赖安装失败，请手动运行: pip install -r requirements.txt"
        fi
        log INFO "依赖安装成功"
        echo "[信息] 依赖安装成功"
    else
        local pygame_ver
        pygame_ver=$("${PYTHON_CMD}" -c "import pygame; print(pygame.version.ver)")
        log INFO "pygame 依赖检查通过 (版本: ${pygame_ver})"
    fi
}

if [[ -f "${SCRIPT_DIR}/requirements.txt" ]]; then
    check_pip_deps
else
    log WARN "缺少 requirements.txt，仅检查 pygame..."
    if ! "${PYTHON_CMD}" -c "import pygame" &>/dev/null; then
        log WARN "缺少 pygame 依赖，尝试自动安装..."
        echo "[警告] 缺少 pygame 依赖，正在自动安装..."
        "${PYTHON_CMD}" -m pip install "pygame>=2.0.0"
        if [[ $? -ne 0 ]]; then
            error_exit "pygame 安装失败，请手动运行: pip install pygame"
        fi
        log INFO "pygame 安装成功"
    fi
fi

# ==================== 虚拟环境检测 ====================
log INFO "正在检测虚拟环境..."

if "${PYTHON_CMD}" -c "import sys; exit(0 if sys.prefix != sys.base_prefix else 1)" &>/dev/null; then
    log INFO "检测到虚拟环境: ${VIRTUAL_ENV:-未知}"
else
    log WARN "未检测到虚拟环境，建议使用虚拟环境运行游戏"
    echo "[警告] 未检测到虚拟环境"
    echo "  建议创建虚拟环境:"
    echo "    python3 -m venv venv"
    echo "    source venv/bin/activate"
    echo "    pip install -r requirements.txt"
fi

# ==================== 图形环境检查 ====================
log INFO "正在检查图形环境..."

if [[ -n "${DISPLAY:-}" ]]; then
    log INFO "检测到 X11 显示环境: DISPLAY=${DISPLAY}"
elif [[ -n "${WAYLAND_DISPLAY:-}" ]]; then
    log INFO "检测到 Wayland 显示环境: WAYLAND_DISPLAY=${WAYLAND_DISPLAY}"
elif [[ "$(uname)" == "Darwin" ]]; then
    log INFO "macOS 环境，图形支持默认可用"
else
    log WARN "未检测到图形显示环境，游戏可能无法正常启动"
    echo "[警告] 未检测到图形显示环境 (DISPLAY/WAYLAND_DISPLAY)"
    echo "  如果通过 SSH 远程连接，请使用 X11 转发: ssh -X"
fi

# ==================== 构建启动参数 ====================
log INFO "正在构建启动参数..."

LAUNCH_ARGS=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --fullscreen|-f)
            LAUNCH_ARGS="${LAUNCH_ARGS} --fullscreen"
            log INFO "参数: 全屏模式"
            ;;
        --fps)
            if [[ -z "${2:-}" ]]; then
                error_exit "--fps 需要一个数值参数"
            fi
            LAUNCH_ARGS="${LAUNCH_ARGS} --fps $2"
            log INFO "参数: 帧率=$2"
            shift
            ;;
        --width)
            if [[ -z "${2:-}" ]]; then
                error_exit "--width 需要一个数值参数"
            fi
            LAUNCH_ARGS="${LAUNCH_ARGS} --width $2"
            log INFO "参数: 窗口宽度=$2"
            shift
            ;;
        --height)
            if [[ -z "${2:-}" ]]; then
                error_exit "--height 需要一个数值参数"
            fi
            LAUNCH_ARGS="${LAUNCH_ARGS} --height $2"
            log INFO "参数: 窗口高度=$2"
            shift
            ;;
        --bgm-volume)
            if [[ -z "${2:-}" ]]; then
                error_exit "--bgm-volume 需要一个数值参数"
            fi
            LAUNCH_ARGS="${LAUNCH_ARGS} --bgm-volume $2"
            log INFO "参数: BGM音量=$2"
            shift
            ;;
        --sfx-volume)
            if [[ -z "${2:-}" ]]; then
                error_exit "--sfx-volume 需要一个数值参数"
            fi
            LAUNCH_ARGS="${LAUNCH_ARGS} --sfx-volume $2"
            log INFO "参数: SFX音量=$2"
            shift
            ;;
        --no-audio)
            LAUNCH_ARGS="${LAUNCH_ARGS} --no-audio"
            log INFO "参数: 禁用音频"
            ;;
        --debug)
            LAUNCH_ARGS="${LAUNCH_ARGS} --debug"
            log INFO "参数: 调试模式"
            ;;
        *)
            log WARN "未知参数: $1"
            echo "[警告] 未知参数: $1"
            LAUNCH_ARGS="${LAUNCH_ARGS} $1"
            ;;
    esac
    shift
done

# ==================== 启动游戏 ====================
log INFO "正在启动游戏..."
log INFO "启动命令: ${PYTHON_CMD} main.py${LAUNCH_ARGS}"

echo ""
echo "============================================================"
echo "  植物大战僵尸 - 正在启动..."
echo "============================================================"
echo ""

cd "${SCRIPT_DIR}"
"${PYTHON_CMD}" main.py ${LAUNCH_ARGS}
EXIT_CODE=$?

if [[ ${EXIT_CODE} -ne 0 ]]; then
    log ERROR "游戏异常退出，退出码: ${EXIT_CODE}"
    echo ""
    echo "[错误] 游戏异常退出 (退出码: ${EXIT_CODE})"
    echo "  请查看日志文件: ${LOG_FILE}"
    echo "  尝试使用 --debug 参数启动以获取更多信息"
    exit ${EXIT_CODE}
fi

log INFO "游戏正常退出"
echo ""
echo "============================================================"
echo "  游戏已退出"
echo "============================================================"

log INFO "启动脚本执行完毕"
exit 0
