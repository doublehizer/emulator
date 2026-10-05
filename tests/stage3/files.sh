#!/bin/sh
# Этап 3: VFS из нескольких файлов в корне (есть двоичный файл).
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
"$ROOT/run.sh" --vfs tests/vfs/files.csv --script tests/scripts/vfs_info.txt
