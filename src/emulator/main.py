"""Точка входа эмулятора."""

from emulator.config import format_config, get_vfs_name, parse_args
from emulator.gui import EmulatorWindow
from emulator.script import run_script_file
from emulator.shell import Shell


def main(argv=None):
    """Прочитать параметры, создать эмулятор и открыть окно.

    :param argv: параметры командной строки; None — взять
        параметры, с которыми запущена программа.
    """
    config = parse_args(argv)
    debug_text = format_config(config)
    print(debug_text)
    shell = Shell(get_vfs_name(config.vfs))
    window = EmulatorWindow(shell)
    window.write(debug_text)
    if config.script is not None:
        window.schedule(run_script_file, window, config.script)
    window.run()


if __name__ == "__main__":
    main()
