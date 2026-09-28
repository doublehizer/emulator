#!/bin/sh
# Этап 2: задан только путь к VFS — имя VFS появится в заголовке.
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
"$ROOT/run.sh" --vfs tests/vfs/demo.csv
