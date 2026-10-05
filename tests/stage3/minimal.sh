#!/bin/sh
# Этап 3: минимальная VFS — только заголовок, корень пустой.
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
"$ROOT/run.sh" --vfs tests/vfs/minimal.csv --script tests/scripts/vfs_info.txt
