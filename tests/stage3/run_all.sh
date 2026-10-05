#!/bin/sh
# Этап 3: запустить все проверки по очереди.
# Следующая проверка начинается после закрытия окна эмулятора.
DIR="$(cd "$(dirname "$0")" && pwd)"
for name in minimal files nested not_found bad_format all_commands; do
    echo
    echo "===== $name.sh ====="
    "$DIR/$name.sh"
done
