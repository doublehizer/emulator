#!/bin/sh
# Этап 3: все команды этапов 1–3 на VFS demo, в конце ошибка.
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
"$ROOT/run.sh" --vfs tests/vfs/demo.csv --script tests/scripts/stage3.txt
