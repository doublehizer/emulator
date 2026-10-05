#!/bin/sh
# Этап 3: VFS в неверном формате — три разных ошибки по очереди.
# Следующий запуск начинается после закрытия окна эмулятора.
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
for name in bad_header bad_base64 no_parent; do
    "$ROOT/run.sh" --vfs "tests/vfs/$name.csv" \
        --script tests/scripts/vfs_info.txt
done
