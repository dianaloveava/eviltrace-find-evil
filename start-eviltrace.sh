#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8765}"
URL="http://${HOST}:${PORT}/"
echo "Starting EvilTrace at ${URL}"
echo "Open ${URL} in your browser. Press Ctrl+C to stop."
python -m eviltrace.server
