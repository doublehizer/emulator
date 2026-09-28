#!/bin/sh
# Этап 2: в скрипте ошибка в строке 3 — выполнение должно остановиться.
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
"$ROOT/run.sh" --vfs tests/vfs/demo.csv --script tests/scripts/error.txt
