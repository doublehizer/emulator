"""Ядро эмулятора: выполнение введённых строк."""

from emulator.commands import COMMANDS
from emulator.errors import CommandError
from emulator.parser import parse_line
from emulator.vfs import Vfs


class Shell:
    """Состояние эмулятора и выполнение команд."""

    def __init__(self, vfs=None):
        """Создать эмулятор.

        :param vfs: загруженная VFS; None — пустая VFS по умолчанию.
        """
        self.vfs = vfs if vfs is not None else Vfs()
        self.running = True

    def execute(self, line):
        """Выполнить одну строку и вернуть текст результата.

        :param line: строка, которую ввёл пользователь.
        :return: текст для вывода (может быть пустым).
        :raises EmulatorError: при любой ошибке выполнения.
        """
        name, args = parse_line(line)
        if name is None:
            return ""
        command = COMMANDS.get(name)
        if command is None:
            raise CommandError(f"{name}: команда не найдена")
        return command(self, args)
