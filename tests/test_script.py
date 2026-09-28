"""Тесты для стартового скрипта."""

import os
import tempfile
import unittest

from emulator.errors import EmulatorError, ScriptError
from emulator.script import read_script, run_script, run_script_file
from emulator.shell import Shell


class FakeWindow:
    """Подмена окна: вместо показа на экране запоминает текст."""

    def __init__(self):
        """Создать подмену окна с новым эмулятором."""
        self.shell = Shell()
        self.lines = []

    def write(self, text, tag="output"):
        """Запомнить выведенный текст."""
        self.lines.append(text)

    def run_line(self, line):
        """Выполнить строку так же, как настоящее окно."""
        self.write(f"$ {line}")
        try:
            result = self.shell.execute(line)
        except EmulatorError as error:
            self.write(f"Ошибка: {error}")
            return False
        if result:
            self.write(result)
        return True


class RunScriptTest(unittest.TestCase):
    """Проверки выполнения строк скрипта."""

    def setUp(self):
        """Создать новое окно-подмену перед каждым тестом."""
        self.window = FakeWindow()

    def test_all_lines_run(self):
        """Скрипт без ошибок выполняется целиком."""
        self.assertTrue(run_script(self.window, ["ls", "cd dir"]))
        self.assertIn("$ ls", self.window.lines)
        self.assertIn("cd ['dir']", self.window.lines)

    def test_stops_on_first_error(self):
        """После ошибки следующие строки не выполняются."""
        success = run_script(self.window, ["ls", "foo", "cd after"])
        self.assertFalse(success)
        self.assertIn(
            "Скрипт остановлен: ошибка в строке 2.", self.window.lines
        )
        self.assertNotIn("$ cd after", self.window.lines)

    def test_empty_lines_skipped(self):
        """Пустые строки пропускаются, но учитываются в нумерации."""
        run_script(self.window, ["", "   ", "foo"])
        self.assertIn(
            "Скрипт остановлен: ошибка в строке 3.", self.window.lines
        )

    def test_stops_after_exit(self):
        """После exit остальные строки не выполняются."""
        self.assertTrue(run_script(self.window, ["exit", "ls"]))
        self.assertNotIn("$ ls", self.window.lines)


class ReadScriptTest(unittest.TestCase):
    """Проверки чтения файла скрипта."""

    def test_read_lines(self):
        """Строки файла читаются по порядку."""
        with tempfile.NamedTemporaryFile(
            "w", suffix=".txt", delete=False, encoding="utf-8"
        ) as file:
            file.write("ls\ncd dir\n")
        try:
            self.assertEqual(read_script(file.name), ["ls", "cd dir"])
        finally:
            os.remove(file.name)

    def test_missing_file(self):
        """Несуществующий файл — ошибка скрипта."""
        with self.assertRaises(ScriptError):
            read_script("no_such_file.txt")

    def test_missing_file_reported(self):
        """Ошибка чтения показывается в окне."""
        window = FakeWindow()
        self.assertFalse(run_script_file(window, "no_such_file.txt"))
        self.assertIn(
            "Ошибка: скрипт не найден: no_such_file.txt", window.lines
        )


if __name__ == "__main__":
    unittest.main()
