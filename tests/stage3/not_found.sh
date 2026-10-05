#!/bin/sh
# Этап 3: файла VFS нет — ошибка загрузки, VFS по умолчанию.
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
"$ROOT/run.sh" --vfs tests/vfs/no_such_file.csv --script tests/scripts/vfs_info.txt
