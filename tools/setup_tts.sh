#!/bin/bash
# Install the free Kokoro voice if it's missing (fresh containers lose it).
set -e
python3 -c "import kokoro_onnx, soundfile" 2>/dev/null || pip install -q kokoro-onnx soundfile
command -v ffmpeg >/dev/null || (apt-get update -q && apt-get install -y -q ffmpeg)
mkdir -p ~/kokoro && cd ~/kokoro
B=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -s kokoro-v1.0.int8.onnx ] || curl -sSLO $B/kokoro-v1.0.int8.onnx
[ -s voices-v1.0.bin ] || curl -sSLO $B/voices-v1.0.bin
echo "tts ready"
