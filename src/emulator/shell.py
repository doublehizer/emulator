"""Ядро эмулятора: выполнение введённых строк."""

from emulator.commands import COMMANDS
from emulator.config import DEFAULT_VFS_NAME
from emulator.errors import CommandError
from emulator.parser import parse_line


class Shell:
    """Состояние эмулятора и выполнение команд."""

    def __init__(self, vfs_name=DEFAULT_VFS_NAME):
        """Создать эмулятор.

        :param vfs_name: имя VFS, показывается в заголовке окна.
        """
        self.vfs_name = vfs_name
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
