#!/bin/sh
# Этап 2: задан только стартовый скрипт без ошибок.
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
"$ROOT/run.sh" --script tests/scripts/ok.txt
