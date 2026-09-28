"""Тесты для параметров запуска."""

import io
import unittest
from contextlib import redirect_stderr

from emulator.config import (
    DEFAULT_VFS_NAME, format_config, get_vfs_name, parse_args,
)


class ParseArgsTest(unittest.TestCase):
    """Проверки чтения параметров командной строки."""

    def test_no_args(self):
        """Без параметров оба поля пустые."""
        config = parse_args([])
        self.assertIsNone(config.vfs)
        self.assertIsNone(config.script)

    def test_all_args(self):
        """Оба параметра читаются."""
        config = parse_args(["--vfs", "a/demo.csv", "--script", "s.txt"])
        self.assertEqual(config.vfs, "a/demo.csv")
        self.assertEqual(config.script, "s.txt")

    def test_unknown_arg(self):
        """Неизвестный параметр — выход с ошибкой."""
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            parse_args(["--color", "red"])


class VfsNameTest(unittest.TestCase):
    """Проверки получения имени VFS."""

    def test_name_from_path(self):
        """Имя — имя файла без расширения."""
        self.assertEqual(get_vfs_name("tests/vfs/demo.csv"), "demo")

    def test_default_name(self):
        """Без пути — имя по умолчанию."""
        self.assertEqual(get_vfs_name(None), DEFAULT_VFS_NAME)


class FormatConfigTest(unittest.TestCase):
    """Проверки отладочного вывода."""

    def test_all_params_shown(self):
        """В выводе есть все параметры и их значения."""
        text = format_config(parse_args(["--vfs", "demo.csv"]))
        self.assertIn("vfs = demo.csv", text)
        self.assertIn("script = не задан", text)


if __name__ == "__main__":
    unittest.main()
