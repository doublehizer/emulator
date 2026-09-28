"""Точка входа эмулятора."""

from emulator.gui import EmulatorWindow
from emulator.shell import Shell


def main():
    """Создать эмулятор и открыть окно."""
    shell = Shell()
    window = EmulatorWindow(shell)
    window.run()


if __name__ == "__main__":
    main()
