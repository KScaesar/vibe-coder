#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <youtube_url>"
    exit 1
fi

URL="$1"

mkdir -p downloads logs
touch downloads/archive.txt

echo "Starting download for: $URL"

# Tip: If you face 403/429 errors, add --cookies-from-browser chrome below
uv tool run yt-dlp \
  --js-runtimes node \
  -f "bv*+ba/b" \
  --merge-output-format mp4 \
  --retries 10 \
  --fragment-retries 10 \
  --concurrent-fragments 4 \
  --continue \
  --no-overwrites \
  --download-archive downloads/archive.txt \
  -o "downloads/%(title)s [%(id)s].%(ext)s" \
  "$URL" \
  2> >(tee "logs/yt-dlp_$(date +%F_%H%M%S).log" >&2)

echo "Download process completed."
