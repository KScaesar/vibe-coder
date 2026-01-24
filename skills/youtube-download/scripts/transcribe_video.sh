#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <video_file_path>"
    exit 1
fi

VIDEO_FILE="$1"

if [ ! -f "$VIDEO_FILE" ]; then
    echo "Error: File '$VIDEO_FILE' not found."
    exit 1
fi

mkdir -p transcripts logs

CORES=$(nproc)
THREADS=$((CORES * 3 / 4))
if [ "$THREADS" -lt 1 ]; then
  THREADS=1
fi

echo "Processing transcript for: $VIDEO_FILE"
echo "Using optimized settings: Device=CPU, Compute=INT8, Threads=$THREADS"

uv tool run whisper-ctranslate2 "$VIDEO_FILE" \
  --model medium \
  --language zh \
  --initial_prompt "以下是繁體中文的逐字稿。" \
  --task transcribe \
  --output_dir transcripts \
  --output_format all \
  --device cpu \
  --compute_type int8 \
  --threads "$THREADS" \
  2> >(tee "logs/whisper_$(date +%F_%H%M%S).log" >&2)

echo "Done. Transcript saved to transcripts/"
