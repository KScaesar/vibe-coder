#!/bin/bash
set -euo pipefail

# Configuration
LOG_DIR="logs"
TRANSCRIPT_DIR="transcripts"

# Ensure directories exist
mkdir -p "$LOG_DIR" "$TRANSCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

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
    log "ERROR" "Script crashed at line $1: '$2'"
}
trap 'error_handler ${LINENO} "$BASH_COMMAND"' ERR

if [ -z "${1:-}" ]; then
    echo "Usage: $0 <video_file_path> [model_size]"
    exit 1
fi

VIDEO_FILE="$1"
MODEL_SIZE="${2:-medium}"

if [ ! -f "$VIDEO_FILE" ]; then
    log "ERROR" "File '$VIDEO_FILE' not found."
    exit 1
fi

# Resource Optimization
CORES=$(nproc)
# Use 75% of cores, minimum 1
THREADS=$((CORES * 3 / 4))
if [ "$THREADS" -lt 1 ]; then THREADS=1; fi

LOG_FILE="$LOG_DIR/whisper_$(date +%Y%m%d_%H%M%S).log"

log "INFO" "Starting transcription for: $VIDEO_FILE"
log "INFO" "Configuration: Model=$MODEL_SIZE, Device=CPU(INT8), Threads=$THREADS"
log "INFO" "Logs: $LOG_FILE"

set +e
uv tool run whisper-ctranslate2 "$VIDEO_FILE" \
  --model "$MODEL_SIZE" \
  --language zh \
  --initial_prompt "以下是繁體中文的逐字稿。" \
  --task transcribe \
  --output_dir "$TRANSCRIPT_DIR" \
  --output_format all \
  --device cpu \
  --compute_type int8 \
  --threads "$THREADS" \
  >> "$LOG_FILE" 2>&1

EXIT_CODE=$?
set -e

if [ $EXIT_CODE -eq 0 ]; then
    log "INFO" "Transcription successful."
    log "INFO" "Output saved to: $TRANSCRIPT_DIR"
else
    log "ERROR" "Transcription failed. See log: $LOG_FILE"
    tail -n 10 "$LOG_FILE"
    exit 1
fi
