#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="${1:-.venv-whisper}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

"$PYTHON_BIN" -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install --upgrade pip setuptools wheel
"$VENV_DIR/bin/python" -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org faster-whisper

echo "faster-whisper environment ready: $VENV_DIR"
echo "Use: $VENV_DIR/bin/python scripts/transcribe_faster_whisper.py <audio> <out_dir>"
