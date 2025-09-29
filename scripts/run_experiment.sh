#!/usr/bin/env bash
set -euo pipefail
python -m src.cli eval --trials "${1:-10}"
