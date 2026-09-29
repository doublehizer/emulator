"""Тесты для ядра эмулятора."""

import unittest

from emulator.errors import CommandError, ParseError
from emulator.shell import Shell


class ShellTest(unittest.TestCase):
    """Проверки выполнения команд через Shell.

    Каждый тест создаёт свой новый Shell, поэтому тесты
    не влияют друг на друга.
    """

    def test_ls_stub(self):
        """ls выводит своё имя и аргументы."""
        shell = Shell("test")
        result = shell.execute("ls -l /home")
        self.assertEqual(result, "ls ['-l', '/home']")

    def test_cd_with_quotes(self):
        """Аргумент в кавычках доходит до cd целиком."""
        shell = Shell("test")
        result = shell.execute('cd "My Documents"')
        self.assertEqual(result, "cd ['My Documents']")

    def test_cd_too_many_args(self):
        """cd с двумя аргументами — ошибка."""
        shell = Shell("test")
        with self.assertRaises(CommandError):
            shell.execute("cd a b")

    def test_unknown_command(self):
        """Неизвестная команда — ошибка."""
        shell = Shell("test")
        with self.assertRaises(CommandError):
            shell.execute("foo")

    def test_unclosed_quote(self):
        """Незакрытая кавычка — ошибка разбора."""
        shell = Shell("test")
        with self.assertRaises(ParseError):
            shell.execute('cd "abc')

    def test_empty_line(self):
        """Пустая строка ничего не делает."""
        shell = Shell("test")
        self.assertEqual(shell.execute("   "), "")

    def test_exit(self):
        """exit останавливает эмулятор."""
        shell = Shell("test")
        shell.execute("exit")
        self.assertFalse(shell.running)

    def test_exit_with_args(self):
        """exit с аргументами — ошибка, эмулятор продолжает работу."""
        shell = Shell("test")
        with self.assertRaises(CommandError):
            shell.execute("exit now")
        self.assertTrue(shell.running)


if __name__ == "__main__":
    unittest.main()
