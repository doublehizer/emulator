#!/bin/sh
# Запуск эмулятора из любой папки.
cd "$(dirname "$0")" || exit 1
PYTHONPATH=src exec python3 -m emulator "$@"
