"""Тесты для виртуальной файловой системы."""

import hashlib
import os
import tempfile
import unittest
from pathlib import Path

from emulator.errors import CommandError, VfsError
from emulator.shell import Shell
from emulator.vfs import VfsDir, VfsFile, count_nodes, load_vfs

VFS_DIR = Path(__file__).parent / "vfs"


def load_text(text):
    """Записать текст во временный CSV-файл и загрузить из него VFS."""
    with tempfile.NamedTemporaryFile(
        "w", suffix=".csv", delete=False, encoding="utf-8"
    ) as file:
        file.write(text)
    try:
        return load_vfs(file.name)
    finally:
        os.remove(file.name)


class LoadVfsTest(unittest.TestCase):
    """Проверки загрузки правильных VFS."""

    def test_minimal(self):
        """Минимальная VFS — пустой корень."""
        vfs = load_vfs(VFS_DIR / "minimal.csv")
        self.assertEqual(vfs.name, "minimal")
        self.assertEqual(vfs.root.children, {})

    def test_files(self):
        """Несколько файлов в корне, двоичный файл раскодирован."""
        vfs = load_vfs(VFS_DIR / "files.csv")
        self.assertEqual(count_nodes(vfs.root), (3, 0))
        data = vfs.root.children["data.bin"].data
        self.assertEqual(data[:2], b"\x00\x11")

    def test_nested(self):
        """Файл на 4-м уровне доступен по цепочке каталогов."""
        vfs = load_vfs(VFS_DIR / "demo.csv")
        user = vfs.root.children["home"].children["user"]
        readme = user.children["docs"].children["readme.txt"]
        self.assertIsInstance(readme, VfsFile)
        self.assertEqual(readme.data.decode("utf-8"), "Привет из VFS!\n")
        self.assertIsInstance(user.children["My Documents"], VfsDir)

    def test_sha256(self):
        """Хеш считается по байтам CSV-файла."""
        path = VFS_DIR / "demo.csv"
        expected = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(load_vfs(path).sha256, expected)


class LoadErrorTest(unittest.TestCase):
    """Проверки ошибок загрузки VFS."""

    def assert_error(self, text, message):
        """Проверить, что загрузка текста даёт ошибку с сообщением."""
        with self.assertRaises(VfsError) as context:
            load_text(text)
        self.assertIn(message, str(context.exception))

    def test_missing_file(self):
        """Несуществующий файл — ошибка."""
        with self.assertRaises(VfsError) as context:
            load_vfs("no_such_file.csv")
        self.assertIn("не найден", str(context.exception))

    def test_bad_header(self):
        """Неверный заголовок — ошибка формата."""
        self.assert_error("a,b,c\n", "первая строка")

    def test_empty_file(self):
        """Пустой файл — ошибка формата."""
        self.assert_error("", "первая строка")

    def test_wrong_columns(self):
        """Не хватает значений в строке."""
        self.assert_error("path,type,content\n/a,dir\n", "строка 2")

    def test_bad_type(self):
        """Неизвестный тип элемента."""
        self.assert_error("path,type,content\n/a,link,\n", "неизвестный тип")

    def test_bad_base64(self):
        """Содержимое файла не в base64."""
        self.assert_error("path,type,content\n/a,file,!!!\n", "base64")

    def test_no_parent(self):
        """Каталог-родитель не описан раньше."""
        self.assert_error(
            "path,type,content\n/x/a,file,\n", "родительский каталог"
        )

    def test_duplicate(self):
        """Один и тот же путь два раза."""
        self.assert_error(
            "path,type,content\n/a,dir,\n/a,dir,\n", "уже есть"
        )

    def test_relative_path(self):
        """Путь не от корня."""
        self.assert_error("path,type,content\na,dir,\n", "начинаться с /")


class VfsInfoTest(unittest.TestCase):
    """Проверки команды vfs-info."""

    def test_loaded_vfs(self):
        """Выводятся имя, хеш и число элементов."""
        vfs = load_vfs(VFS_DIR / "demo.csv")
        result = Shell(vfs).execute("vfs-info")
        self.assertIn("Имя VFS: demo", result)
        self.assertIn(f"SHA-256: {vfs.sha256}", result)
        self.assertIn("Каталогов: 6, файлов: 5", result)

    def test_default_vfs(self):
        """Без загруженной VFS — VFS по умолчанию."""
        result = Shell().execute("vfs-info")
        self.assertIn("Имя VFS: default", result)

    def test_with_args(self):
        """Аргументы у vfs-info — ошибка."""
        with self.assertRaises(CommandError):
            Shell().execute("vfs-info now")


if __name__ == "__main__":
    unittest.main()
