"""Тесты для парсера командной строки."""

import unittest

from emulator.errors import ParseError
from emulator.parser import parse_line


class ParseLineTest(unittest.TestCase):
    """Проверки функции parse_line."""

    def test_command_without_args(self):
        """Команда без аргументов."""
        self.assertEqual(parse_line("ls"), ("ls", []))

    def test_command_with_args(self):
        """Аргументы разделяются пробелами."""
        self.assertEqual(parse_line("ls -l /home"), ("ls", ["-l", "/home"]))

    def test_double_quotes(self):
        """Текст в двойных кавычках — один аргумент."""
        self.assertEqual(
            parse_line('cd "My Documents"'), ("cd", ["My Documents"])
        )

    def test_single_quotes(self):
        """Текст в одинарных кавычках — один аргумент."""
        self.assertEqual(parse_line("ls 'a b' c"), ("ls", ["a b", "c"]))

    def test_empty_line(self):
        """Пустая строка — нет команды."""
        self.assertEqual(parse_line("   "), (None, []))

    def test_unclosed_quote(self):
        """Незакрытая кавычка — ошибка разбора."""
        with self.assertRaises(ParseError):
            parse_line('cd "My Documents')

    def test_unclosed_quote_message(self):
        """Сообщение об ошибке понятно пользователю."""
        with self.assertRaises(ParseError) as context:
            parse_line("ls 'abc")
        self.assertIn("не закрыта кавычка", str(context.exception))


if __name__ == "__main__":
    unittest.main()
