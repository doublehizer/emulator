#!/bin/sh
# Этап 3: VFS с 4 уровнями каталогов и файлов.
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
"$ROOT/run.sh" --vfs tests/vfs/demo.csv --script tests/scripts/vfs_info.txt
