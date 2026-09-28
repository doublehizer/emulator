#!/bin/sh
# Этап 2: указан несуществующий скрипт — ошибка чтения скрипта.
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
"$ROOT/run.sh" --script tests/scripts/no_such_file.txt
