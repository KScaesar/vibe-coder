---
name: youtube-download
description: Production-ready workflow for downloading YouTube videos, extracting lossless clips, and generating AI transcripts. Use when you need to download videos, clip specific segments, archive channels, generate subtitles (SRT/VTT), or create text transcripts for RAG/indexing from YouTube URLs. Supports both CPU and GPU environments.
---

# YouTube Download Skill

A production-ready, idempotent workflow for downloading YouTube videos, extracting specific segments, and generating high-quality transcripts using AI.

## Core Capabilities
- **Reliable Downloading**: Uses `yt-dlp` with best-practice flags for retries, resumption, and deduplication.
- **AI Transcription**: Uses `whisper-ctranslate2` (optimized) for speech-to-text.
- **Format Flexibility**: Outputs raw video (mp4) and transcripts (txt, srt, vtt, json, tsv).
- **Environment Isolation**: Uses `uv tool` to prevent Python dependency conflicts.
- **Video Clipping**: Lossless extraction of specific video segments using `ffmpeg`.

## Installation & Setup

### 1. System Dependencies (Debian/Ubuntu)
```bash
sudo apt-get update && sudo apt-get install -y ffmpeg
ffmpeg -version  # Verify installation
```

### 2. Install Tools via `uv`
```bash
# Video Downloader
uv tool install yt-dlp

# AI Transcriber
uv tool install whisper-ctranslate2
```

## Usage Patterns

The skill includes scripts in the `scripts/` directory.

### Scenario 1: One-Click Automation (Download + Transcribe)
Use the wrapper script `scripts/download_and_transcribe.sh` for the simplest workflow.

```bash
chmod +x scripts/*.sh
./scripts/download_and_transcribe.sh "https://www.youtube.com/watch?v=VIDEO_ID"
```
*Logic*: Checks `downloads/archive.txt`. If video exists, skips download and proceeds to transcription. If transcript exists, it will overwrite (unless script modified).

### Scenario 2: Download Only (Best Quality)
Best for archiving without immediate transcription.

```bash
./scripts/download_video.sh "URL"
```

### Scenario 3: Transcribe Only (High Performance CPU)
Best for processing existing files or re-running transcription with different settings.

```bash
./scripts/transcribe_video.sh "downloads/video.mp4"
```

### Scenario 4: Handling 403 / 429 / Login Issues (Authenticated)
Use this method when facing HTTP 403 (Forbidden), 429 (Too Many Requests), or Age-Gated content. This is the **most stable** method as it uses your browser's cookies.

```bash
yt-dlp \
  --js-runtimes node \
  --cookies-from-browser chrome \
  -f "bv*+ba/b" \
  --merge-output-format mp4 \
  --retries 10 \
  --fragment-retries 10 \
  --concurrent-fragments 4 \
  --continue \
  --no-overwrites \
  --download-archive downloads/archive.txt \
  -o "downloads/%(title)s [%(id)s].%(ext)s" \
  "URL" \
  2> "logs/yt-dlp_$(date +%F_%H%M%S).log"
```

**Security Warning**:
- **Cookies are equivalent to login credentials.**
- **NEVER** commit, upload, or share cookie files or commands containing raw cookie data.
- On server environments, ensure cookie files (if used) have strict permissions: `chmod 600`.

### Scenario 5: Video Clipping (Lossless & Fast)
Extract specific segments from a video without re-encoding (no quality loss). Best for creating clips for pronunciation practice, highlights, or datasets.

Use the helper script:
```bash
./scripts/clip_video.sh "input.mp4" "22:41" "28:44" "output_clip.mp4"
```

Or run `ffmpeg` directly:
```bash
# Syntax: ffmpeg -ss <START> -to <END> -i <INPUT> -c copy <OUTPUT>
ffmpeg -ss 22:41 -to 28:44 -i "video.mp4" -c copy "clip_name.mp4"
```

**Key Parameters:**
- `-ss`: Start time (HH:MM:SS). Placed **before** `-i` for fast seeking.
- `-to`: End time (HH:MM:SS).
- `-c copy`: **Critical**. Copies streams directly without re-encoding. Extremely fast and preserves original quality.

## Directory Structure (Standard)
Maintain this structure for idempotent automation:

```text
.
├── downloads/
│   ├── archive.txt        # Deduplication log (Critical for idempotency)
│   └── *.mp4              # Source videos
├── transcripts/           # Generated outputs
│   ├── *.txt              # Raw text for NLP/RAG
│   ├── *.srt              # Subtitles
│   └── *.json             # Metadata & timestamps
└── logs/                  # Execution logs
```

## Troubleshooting
- **Slow Transcription**: Ensure `whisper-ctranslate2` is used with `--compute_type int8` on CPU.
- **Download Fails**: Update `yt-dlp` (`uv tool upgrade yt-dlp`).
- **OOM (Out of Memory)**: Reduce `--threads` count or switch from `medium` to `small` model.
