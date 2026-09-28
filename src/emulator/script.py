"""Выполнение стартового скрипта эмулятора.

Скрипт — текстовый файл с командами эмулятора, по одной на строку.
Команды выполняются так, как будто их по очереди вводит пользователь.
"""

from emulator.errors import ScriptError


def read_script(path):
    """Прочитать строки стартового скрипта.

    :param path: путь к файлу скрипта.
    :return: список строк файла.
    :raises ScriptError: если файл не найден или не читается.
    """
    try:
        with open(path, encoding="utf-8") as file:
            return file.read().splitlines()
    except FileNotFoundError as error:
        raise ScriptError(f"скрипт не найден: {path}") from error
    except (OSError, UnicodeDecodeError) as error:
        raise ScriptError(f"не удалось прочитать скрипт: {path}") from error


def run_script(window, lines):
    """Выполнить строки скрипта по очереди.

    Пустые строки пропускаются. На первой ошибке выполнение
    останавливается, и выводится номер строки с ошибкой.

    :param window: окно эмулятора (нужны run_line, write и shell).
    :param lines: строки скрипта.
    :return: True, если скрипт выполнен без ошибок.
    """
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        if not window.run_line(line):
            window.write(
                f"Скрипт остановлен: ошибка в строке {number}.", "error"
            )
            return False
        if not window.shell.running:
            return True
    return True


def run_script_file(window, path):
    """Прочитать скрипт из файла и выполнить его в окне.

    :param window: окно эмулятора.
    :param path: путь к файлу скрипта.
    :return: True, если скрипт выполнен без ошибок.
    """
    try:
        lines = read_script(path)
    except ScriptError as error:
        window.write(f"Ошибка: {error}", "error")
        return False
    window.write(f"--- Выполнение стартового скрипта: {path} ---")
    success = run_script(window, lines)
    if success and window.shell.running:
        window.write("--- Скрипт выполнен ---")
    return success
