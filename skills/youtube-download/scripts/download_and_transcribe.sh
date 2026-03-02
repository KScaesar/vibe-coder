#!/bin/bash
set -euo pipefail

DOWNLOAD_DIR="downloads"
TRANSCRIPT_DIR="transcripts"

mkdir -p "$DOWNLOAD_DIR" "$TRANSCRIPT_DIR" "logs"

# Logging (Simplified)
log() {
    echo "[$(date +'%H:%M:%S')] $1"
}

if [ -z "${1:-}" ]; then
    echo "Usage: $0 <URL>"
    exit 1
fi

URL="$1"
log "Workflow Started: $URL"

# Step 1: Get filename (Dry Run)
# We need to know what file yt-dlp *will* create to pass it to the transcriber.
# Note: This is tricky if yt-dlp format changes or download fails.
log "Resolving filename..."
FILES=$(uv tool run yt-dlp \
    --print filename \
    --merge-output-format mp4 \
    --no-playlist \
    -o "$DOWNLOAD_DIR/%(title)s [%(id)s].%(ext)s" \
    "$URL")

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Step 2: Download
log "Initiating Download Phase..."
"$SCRIPT_DIR/download_video.sh" "$URL"

# Step 3: Transcribe
IFS=$'\n'
for FILE_PATH in $FILES; do
    # Check if file exists (it should, if download succeeded)
    if [ -f "$FILE_PATH" ]; then
        log "File found: $FILE_PATH"
        log "Initiating Transcription Phase..."
        "$SCRIPT_DIR/transcribe_video.sh" "$FILE_PATH"
    else
        log "WARNING: File not found: $FILE_PATH"
        log "Download might have failed, or filename mismatch."
    fi
done
unset IFS

log "Workflow Complete."
