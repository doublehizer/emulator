"""Точка входа эмулятора."""

from emulator.config import format_config, parse_args
from emulator.errors import VfsError
from emulator.gui import EmulatorWindow
from emulator.script import run_script_file
from emulator.shell import Shell
from emulator.vfs import Vfs, load_vfs


def open_vfs(path):
    """Загрузить VFS, если путь к ней задан.

    :param path: путь к CSV-файлу VFS или None.
    :return: кортеж ``(vfs, ошибка)``. Если путь не задан или
        загрузить не удалось, вместо VFS будет пустая VFS
        по умолчанию. Ошибка — текст или None.
    """
    if path is None:
        return Vfs(), None
    try:
        return load_vfs(path), None
    except VfsError as error:
        return Vfs(), f"Ошибка загрузки VFS: {error}"


def main(argv=None):
    """Прочитать параметры, загрузить VFS, создать эмулятор и окно.

    :param argv: параметры командной строки; None — взять
        параметры, с которыми запущена программа.
    """
    config = parse_args(argv)
    debug_text = format_config(config)
    print(debug_text)
    vfs, vfs_error = open_vfs(config.vfs)
    shell = Shell(vfs)
    window = EmulatorWindow(shell)
    window.write(debug_text)
    if vfs_error is not None:
        print(vfs_error)
        window.write(vfs_error, "error")
    if config.script is not None:
        window.schedule(run_script_file, window, config.script)
    window.run()


if __name__ == "__main__":
    main()
