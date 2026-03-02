#!/bin/bash
set -euo pipefail

if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <input_video> <start_time> <end_time> [output_name]"
    echo "Example: $0 video.mp4 22:41 28:44 my_clip.mp4"
    exit 1
fi

INPUT="$1"
START="$2"
END="$3"
OUTPUT="${4:-}"

if [ ! -f "$INPUT" ]; then
    echo "Error: Input file '$INPUT' not found."
    exit 1
fi

if [ -z "$OUTPUT" ]; then
    FILENAME=$(basename -- "$INPUT")
    EXTENSION="${FILENAME##*.}"
    BASENAME="${FILENAME%.*}"
    SAFE_START=${START//:/}
    SAFE_END=${END//:/}
    OUTPUT="${BASENAME}_clip_${SAFE_START}-${SAFE_END}.${EXTENSION}"
fi

echo "Clipping video: $INPUT"
echo "Start: $START | End: $END"
echo "Output: $OUTPUT"

ffmpeg -ss "$START" -to "$END" -i "$INPUT" -c copy "$OUTPUT"

echo "Clip created successfully: $OUTPUT"
