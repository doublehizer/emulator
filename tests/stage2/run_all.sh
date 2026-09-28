#!/bin/sh
# Этап 2: запустить все проверки по очереди.
# Следующая проверка начинается после закрытия окна эмулятора.
DIR="$(cd "$(dirname "$0")" && pwd)"
for name in no_args vfs_only script_only all_params \
            script_error script_missing bad_option; do
    echo
    echo "===== $name.sh ====="
    "$DIR/$name.sh"
done
