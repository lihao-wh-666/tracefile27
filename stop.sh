#!/usr/bin/env bash
# ============================================================
#  Plants vs Zombies - Linux/macOS Stop Script (stop.sh)
#  Feature: Find and terminate game processes
#  Usage: ./stop.sh [options]
#    --force / -f    Force kill (SIGKILL)
#    --help / -h     Show help
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/game_launch.log"

# ==================== Log Function ====================
log() {
    local level="$1"
    shift
    local msg="$*"
    local timestamp
    timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    local entry="[${timestamp}] [${level}] ${msg}"
    echo "${entry}" >> "${LOG_FILE}"
    case "${level}" in
        ERROR) echo "[ERROR] ${msg}" ;;
        WARN)  echo "[WARN] ${msg}" ;;
    esac
}

# ==================== Show Help ====================
show_help() {
    cat <<EOF

============================================================
  Plants vs Zombies - Stop Script Help
============================================================

Usage: ./stop.sh [options]

Options:
  --force / -f    Force kill processes immediately (SIGKILL)
  --help / -h     Show this help

Examples:
  ./stop.sh              Gracefully stop game (SIGTERM)
  ./stop.sh --force      Force kill game processes (SIGKILL)
  ./stop.sh -f           Same as above

Notes:
  - If graceful termination fails, use --force
  - All processes running 'python* main.py' will be stopped
  - Logs are written to game_launch.log

EOF
}

# ==================== Error Exit ====================
error_exit() {
    log ERROR "$1"
    exit 1
}

# ==================== Script Start ====================
log INFO "Stop script started"

# Check help option
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    show_help
    exit 0
fi

# Parse args
FORCE_KILL=0
if [[ "${1:-}" == "--force" || "${1:-}" == "-f" ]]; then
    FORCE_KILL=1
fi

# ==================== Header ====================
echo ""
echo "============================================================"
echo "  Plants vs Zombies - Stop Game"
echo "============================================================"
echo ""

log INFO "Searching for game processes..."

# Find processes running main.py
# Match patterns: python main.py, python3 main.py, python3.11 main.py, etc.
PROCESS_IDS=$(pgrep -f "python[0-9.]* main\.py" 2>/dev/null || true)

if [[ -z "${PROCESS_IDS}" ]]; then
    log INFO "No game processes found"
    echo "[INFO] No game processes found running."
    log INFO "Stop script finished"
    exit 0
fi

# Count processes
PROCESS_COUNT=$(echo "${PROCESS_IDS}" | wc -w)
log INFO "Found ${PROCESS_COUNT} game process(es)"

echo "Found ${PROCESS_COUNT} game process(es):"
for pid in ${PROCESS_IDS}; do
    # Get process command line
    if command -v ps &>/dev/null; then
        cmd=$(ps -p "${pid}" -o args= 2>/dev/null || echo "PID ${pid}")
    else
        cmd="PID ${pid}"
    fi
    echo "  - ${pid}: ${cmd}"
    log INFO "Found game process PID: ${pid}"
done
echo ""

# ==================== Terminate ====================
if [[ ${FORCE_KILL} -eq 1 ]]; then
    log INFO "Force killing game processes (SIGKILL)..."
    echo "[INFO] Force killing game processes (SIGKILL)..."
    SIGNAL="-9"
else
    log INFO "Gracefully terminating game processes (SIGTERM)..."
    echo "[INFO] Terminating game processes (SIGTERM)..."
    SIGNAL="-15"
fi

FAILED=0
KILLED=0
for pid in ${PROCESS_IDS}; do
    if kill ${SIGNAL} "${pid}" 2>/dev/null; then
        log INFO "Successfully killed PID ${pid}"
        echo "  [OK] Killed PID ${pid}"
        KILLED=$((KILLED + 1))
    else
        log ERROR "Failed to kill PID ${pid}"
        echo "  [FAIL] Failed to kill PID ${pid}"
        FAILED=$((FAILED + 1))
    fi
done

# If graceful kill had failures and we didn't use force, suggest --force
if [[ ${FAILED} -gt 0 && ${FORCE_KILL} -eq 0 ]]; then
    log WARN "Some processes could not be terminated, suggest using --force"
    echo ""
    echo "[WARN] Some processes could not be terminated."
    echo "       Use --force or -f to force kill them."
fi

echo ""
log INFO "Stop operation completed. Killed: ${KILLED}, Failed: ${FAILED}"
echo "============================================================"
echo "  Stop operation completed. Killed: ${KILLED}, Failed: ${FAILED}"
echo "============================================================"

log INFO "Stop script finished"

if [[ ${FAILED} -gt 0 ]]; then
    exit 1
else
    exit 0
fi
