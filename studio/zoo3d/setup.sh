#!/bin/bash
# Fresh-container setup for the 3D sing-along pipeline (song engine + finishing + optional bpy previews).
set -e
pip install --break-system-packages -q pyworld soundfile kokoro-onnx fonttools brotli numpy 2>/dev/null || true
D=/root/.cache/hyperframes/tts
if [ ! -f $D/models/kokoro-v1.0.onnx ]; then
  if command -v hyperframes >/dev/null; then hyperframes tts "hello" -o /tmp/_warm.wav >/dev/null 2>&1 || true; fi
fi
if [ ! -f $D/models/kokoro-v1.0.onnx ]; then
  mkdir -p $D/models $D/voices
  curl -sL -o $D/models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
  curl -sL -o $D/voices/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
fi
mkdir -p ~/.fonts && cp "$(dirname "$0")"/fonts/*.ttf ~/.fonts/ 2>/dev/null && fc-cache -f >/dev/null 2>&1 || true
if [ ! -x /root/bpyenv/bin/python ] && command -v uv >/dev/null; then
  uv venv /root/bpyenv -p 3.11 -q && uv pip install --python /root/bpyenv -q bpy==5.0.1 || echo "bpy preview env not installed (optional)"
fi
echo "setup ok"
