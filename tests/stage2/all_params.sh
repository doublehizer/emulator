#!/bin/sh
# Этап 2: заданы оба параметра — путь к VFS и стартовый скрипт.
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
"$ROOT/run.sh" --vfs tests/vfs/demo.csv --script tests/scripts/ok.txt
