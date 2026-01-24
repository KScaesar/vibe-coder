#!/bin/bash
set -e

DOWNLOAD_DIR="downloads"
TRANSCRIPT_DIR="transcripts"
ARCHIVE_FILE="$DOWNLOAD_DIR/archive.txt"

mkdir -p "$DOWNLOAD_DIR" "$TRANSCRIPT_DIR" "logs"

URL="$1"
if [ -z "$URL" ]; then
    echo "Usage: $0 <URL>"
    exit 1
fi

echo "Processing URL: $URL"

FILES=$(uv tool run yt-dlp \
    --print filename \
    --merge-output-format mp4 \
    -o "$DOWNLOAD_DIR/%(title)s [%(id)s].%(ext)s" \
    "$URL")

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/download_video.sh" "$URL"

IFS=$'\n'
for FILE_PATH in $FILES; do
    if [ -f "$FILE_PATH" ]; then
        echo "Found file: $FILE_PATH"
        "$SCRIPT_DIR/transcribe_video.sh" "$FILE_PATH"
    else
        echo "Warning: File not found: $FILE_PATH"
        echo "It might have been skipped or named differently?"
    fi
done
unset IFS

echo "Workflow Complete."
