"""Параметры запуска эмулятора из командной строки."""

import argparse
from pathlib import Path

DEFAULT_VFS_NAME = "default"
NOT_SET = "не задан"


def parse_args(argv=None):
    """Разобрать параметры командной строки.

    :param argv: список параметров; None — взять параметры,
        с которыми запущена программа.
    :return: объект с полями ``vfs`` и ``script``.
        Если параметр не указан, в поле будет None.
    """
    parser = argparse.ArgumentParser(
        prog="emulator",
        description="Эмулятор командной строки UNIX (вариант 12).",
    )
    parser.add_argument(
        "--vfs", help="путь к физическому расположению VFS"
    )
    parser.add_argument(
        "--script", help="путь к стартовому скрипту"
    )
    return parser.parse_args(argv)


def get_vfs_name(vfs_path):
    """Получить имя VFS по пути к ней.

    Имя — это имя файла без расширения: ``data/demo.csv`` → ``demo``.

    :param vfs_path: путь к VFS или None.
    :return: имя VFS; если путь не задан — имя по умолчанию.
    """
    if vfs_path is None:
        return DEFAULT_VFS_NAME
    return Path(vfs_path).stem


def format_config(config):
    """Сформировать текст отладочного вывода параметров.

    :param config: результат parse_args.
    :return: многострочный текст со всеми параметрами.
    """
    lines = ["Параметры запуска:"]
    for name, value in vars(config).items():
        shown = NOT_SET if value is None else value
        lines.append(f"  {name} = {shown}")
    return "\n".join(lines)
