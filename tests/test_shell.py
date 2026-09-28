"""Тесты для ядра эмулятора."""

import unittest

from emulator.errors import CommandError, ParseError
from emulator.shell import Shell


class ShellTest(unittest.TestCase):
    """Проверки выполнения команд через Shell."""

    def setUp(self):
        """Создать новый эмулятор перед каждым тестом."""
        self.shell = Shell("test")

    def test_ls_stub(self):
        """ls выводит своё имя и аргументы."""
        result = self.shell.execute("ls -l /home")
        self.assertEqual(result, "ls ['-l', '/home']")

    def test_cd_with_quotes(self):
        """Аргумент в кавычках доходит до cd целиком."""
        result = self.shell.execute('cd "My Documents"')
        self.assertEqual(result, "cd ['My Documents']")

    def test_cd_too_many_args(self):
        """cd с двумя аргументами — ошибка."""
        with self.assertRaises(CommandError):
            self.shell.execute("cd a b")

    def test_unknown_command(self):
        """Неизвестная команда — ошибка."""
        with self.assertRaises(CommandError):
            self.shell.execute("foo")

    def test_unclosed_quote(self):
        """Незакрытая кавычка — ошибка разбора."""
        with self.assertRaises(ParseError):
            self.shell.execute('cd "abc')

    def test_empty_line(self):
        """Пустая строка ничего не делает."""
        self.assertEqual(self.shell.execute("   "), "")

    def test_exit(self):
        """exit останавливает эмулятор."""
        self.shell.execute("exit")
        self.assertFalse(self.shell.running)

    def test_exit_with_args(self):
        """exit с аргументами — ошибка, эмулятор продолжает работу."""
        with self.assertRaises(CommandError):
            self.shell.execute("exit now")
        self.assertTrue(self.shell.running)


if __name__ == "__main__":
    unittest.main()
