#!/bin/bash
set -euo pipefail

# Configuration
LOG_DIR="logs"
DOWNLOAD_DIR="downloads"
ARCHIVE_FILE="$DOWNLOAD_DIR/archive.txt"

# Ensure directories exist
mkdir -p "$LOG_DIR" "$DOWNLOAD_DIR"
touch "$ARCHIVE_FILE"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    local level=$1
    shift
    local color=$NC
    if [ "$level" == "ERROR" ]; then color=$RED; fi
    if [ "$level" == "WARN" ]; then color=$YELLOW; fi
    if [ "$level" == "INFO" ]; then color=$GREEN; fi
    
    echo -e "${color}[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $*${NC}"
}

error_handler() {
    local line_no=$1
    local command=$2
    # Only report if not inside the handled sub-functions
    log "ERROR" "Script crashed at line $line_no: '$command'"
}
trap 'error_handler ${LINENO} "$BASH_COMMAND"' ERR

# Check dependencies
if ! command -v uv &> /dev/null; then
    log "ERROR" "'uv' is not installed. Please install it first."
    exit 1
fi

# Input validation
if [ -z "${1:-}" ]; then
    echo "Usage: $0 <youtube_url> [additional_args]"
    exit 1
fi

URL="$1"
shift
EXTRA_ARGS="${*:-}" # Pass rest of args to yt-dlp

# Unique log file for this run
LOG_FILE="$LOG_DIR/yt-dlp_$(date +%Y%m%d_%H%M%S).log"

log "INFO" "Starting download task for: $URL"
log "INFO" "Logs will be written to: $LOG_FILE"

# Helper to run yt-dlp
run_ytdlp() {
    local strategy_name="$1"
    shift
    local cookie_args="$@"
    
    log "INFO" "Attempting download strategy: $strategy_name"
    
    # We turn off 'set -e' temporarily to capture the exit code manually
    set +e
    
    # Construct command
    # Using 'eval' or arrays is tricky with 'uv tool run', so we stick to simple expansion
    # Note: --no-playlist is default here to prevent accidents, unless user overrides
    
    uv tool run yt-dlp \
        --js-runtimes node \
        -f "bv*+ba/b" \
        --merge-output-format mp4 \
        --retries 5 \
        --fragment-retries 5 \
        --concurrent-fragments 4 \
        --continue \
        --no-overwrites \
        --download-archive "$ARCHIVE_FILE" \
        --no-playlist \
        -o "$DOWNLOAD_DIR/%(title)s [%(id)s].%(ext)s" \
        $cookie_args \
        $EXTRA_ARGS \
        "$URL" \
        >> "$LOG_FILE" 2>&1
    
    local exit_code=$?
    set -e
    
    if [ $exit_code -eq 0 ]; then
        log "INFO" "Success: Download completed ($strategy_name)."
        return 0
    else
        log "WARN" "Failed: Strategy '$strategy_name' (Exit Code: $exit_code)."
        return 1
    fi
}

# --- Strategy 1: Standard Download ---
if run_ytdlp "Standard (No Cookies)"; then
    log "INFO" "Process finished successfully."
    exit 0
fi

# --- Failure Analysis & Recovery ---
log "INFO" "Analyzing failure reason from logs..."

REASON="Unknown"
NEEDS_COOKIES=false

if grep -q "HTTP Error 403" "$LOG_FILE" || grep -q "Sign in to confirm your age" "$LOG_FILE"; then
    REASON="403 Forbidden / Age Gate"
    NEEDS_COOKIES=true
elif grep -q "Video unavailable" "$LOG_FILE"; then
    REASON="Video Unavailable (Deleted/Private)"
elif grep -q "Too Many Requests" "$LOG_FILE" || grep -q "429" "$LOG_FILE"; then
    REASON="429 Too Many Requests (IP Ban)"
    NEEDS_COOKIES=true
fi

log "WARN" "Detected failure reason: $REASON"

if [ "$NEEDS_COOKIES" = true ]; then
    log "INFO" "Attempting browser cookie extraction..."
    
    # --- Strategy 2: Chrome Cookies ---
    if run_ytdlp "Chrome Cookies" "--cookies-from-browser" "chrome"; then
        log "INFO" "Process finished successfully (used Chrome cookies)."
        exit 0
    fi
    
    # --- Strategy 3: Firefox Cookies ---
    if run_ytdlp "Firefox Cookies" "--cookies-from-browser" "firefox"; then
        log "INFO" "Process finished successfully (used Firefox cookies)."
        exit 0
    fi
    
    log "ERROR" "All cookie strategies failed. Check if you are logged in to YouTube on Chrome/Firefox."
fi

# Final Status
log "ERROR" "Critical Failure. Please inspect the log file:"
echo "      $LOG_FILE"
echo "------------------- [Last 10 lines of log] -------------------"
tail -n 10 "$LOG_FILE"
echo "--------------------------------------------------------------"
exit 1
