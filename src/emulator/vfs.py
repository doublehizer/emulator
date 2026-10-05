"""Виртуальная файловая система (VFS), которая хранится в памяти.

VFS загружается из CSV-файла с колонками ``path,type,content``:

- ``path`` — полный путь от корня, например ``/home/user/notes.txt``;
- ``type`` — ``dir`` (каталог) или ``file`` (файл);
- ``content`` — содержимое файла в base64 (у каталога — пусто).

Вложенность задаётся путём: ``/home/user`` лежит внутри ``/home``.
Каталог должен быть описан раньше, чем то, что в нём лежит.
Файл на диске только читается и никогда не изменяется.
"""

import base64
import csv
import hashlib

from emulator.config import DEFAULT_VFS_NAME, get_vfs_name
from emulator.errors import VfsError

CSV_HEADER = ["path", "type", "content"]
TYPE_DIR = "dir"
TYPE_FILE = "file"
PATH_SEP = "/"


class VfsDir:
    """Каталог VFS: хранит вложенные файлы и каталоги по именам."""

    def __init__(self):
        """Создать пустой каталог."""
        self.children = {}


class VfsFile:
    """Файл VFS: хранит содержимое в виде байтов."""

    def __init__(self, data):
        """Создать файл с заданным содержимым.

        :param data: содержимое файла (bytes).
        """
        self.data = data


class Vfs:
    """Загруженная VFS: имя, корневой каталог и хеш данных."""

    def __init__(self, name=DEFAULT_VFS_NAME, root=None, data=b""):
        """Создать VFS.

        Без параметров получается пустая VFS по умолчанию.

        :param name: имя VFS.
        :param root: корневой каталог; None — пустой каталог.
        :param data: исходные байты CSV-файла, по ним считается хеш.
        """
        self.name = name
        self.root = root if root is not None else VfsDir()
        self.sha256 = hashlib.sha256(data).hexdigest()


def load_vfs(path):
    """Загрузить VFS из CSV-файла в память.

    :param path: путь к CSV-файлу.
    :return: объект Vfs.
    :raises VfsError: если файл не найден или формат неверный.
    """
    data = read_vfs_file(path)
    root = parse_csv(data)
    return Vfs(get_vfs_name(path), root, data)


def read_vfs_file(path):
    """Прочитать CSV-файл VFS целиком.

    :param path: путь к файлу.
    :return: содержимое файла (bytes).
    :raises VfsError: если файл не найден или не читается.
    """
    try:
        with open(path, "rb") as file:
            return file.read()
    except FileNotFoundError as error:
        raise VfsError(f"файл VFS не найден: {path}") from error
    except OSError as error:
        raise VfsError(f"не удалось прочитать VFS: {path}") from error


def parse_csv(data):
    """Построить дерево каталогов и файлов по данным CSV.

    Номера строк в сообщениях об ошибках — как в файле
    (строка 1 — заголовок).

    :param data: содержимое CSV-файла (bytes).
    :return: корневой каталог VfsDir.
    :raises VfsError: если формат неверный.
    """
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise VfsError("неверный формат VFS: файл не в UTF-8") from error
    rows = list(csv.reader(text.splitlines()))
    if not rows or rows[0] != CSV_HEADER:
        raise VfsError(
            "неверный формат VFS: первая строка должна быть path,type,content"
        )
    root = VfsDir()
    for number, row in enumerate(rows[1:], start=2):
        if not row:
            continue
        try:
            add_row(root, row)
        except VfsError as error:
            raise VfsError(
                f"неверный формат VFS, строка {number}: {error}"
            ) from error
    return root


def add_row(root, row):
    """Добавить в дерево один каталог или файл из строки CSV.

    :param root: корневой каталог.
    :param row: список значений строки CSV.
    :raises VfsError: если строка неверная.
    """
    if len(row) != len(CSV_HEADER):
        raise VfsError(f"нужно {len(CSV_HEADER)} значения через запятую")
    path, node_type, content = row
    names = split_path(path)
    parent = find_parent(root, names[:-1], path)
    name = names[-1]
    if name in parent.children:
        raise VfsError(f"{path}: такой путь уже есть")
    parent.children[name] = make_node(node_type, content)


def split_path(path):
    """Разделить путь на имена: ``/home/user`` → ``['home', 'user']``.

    :param path: путь от корня.
    :return: список имён.
    :raises VfsError: если путь не от корня или это сам корень.
    """
    if not path.startswith(PATH_SEP):
        raise VfsError(f"{path}: путь должен начинаться с /")
    names = [name for name in path.split(PATH_SEP) if name]
    if not names:
        raise VfsError("корневой каталог / указывать не нужно")
    return names


def find_parent(root, names, path):
    """Найти каталог, в который нужно положить новый элемент.

    :param root: корневой каталог.
    :param names: имена каталогов от корня до родителя.
    :param path: полный путь (только для сообщения об ошибке).
    :return: каталог-родитель VfsDir.
    :raises VfsError: если такого каталога нет.
    """
    node = root
    for name in names:
        node = node.children.get(name)
        if not isinstance(node, VfsDir):
            raise VfsError(f"{path}: родительский каталог не найден")
    return node


def make_node(node_type, content):
    """Создать каталог или файл по типу из CSV.

    :param node_type: ``dir`` или ``file``.
    :param content: содержимое файла в base64.
    :return: VfsDir или VfsFile.
    :raises VfsError: если тип неизвестен или содержимое неверное.
    """
    if node_type == TYPE_DIR:
        if content:
            raise VfsError("у каталога не может быть содержимого")
        return VfsDir()
    if node_type == TYPE_FILE:
        return VfsFile(decode_content(content))
    raise VfsError(f"неизвестный тип {node_type!r}, нужен dir или file")


def decode_content(content):
    """Раскодировать содержимое файла из base64 в байты.

    :param content: строка base64.
    :return: байты файла.
    :raises VfsError: если строка не в формате base64.
    """
    try:
        return base64.b64decode(content, validate=True)
    except ValueError as error:
        raise VfsError("содержимое файла не в формате base64") from error


def count_nodes(directory):
    """Посчитать файлы и каталоги внутри каталога на всех уровнях.

    :param directory: каталог VfsDir.
    :return: кортеж ``(файлов, каталогов)``.
    """
    files, dirs = 0, 0
    for node in directory.children.values():
        if isinstance(node, VfsDir):
            sub_files, sub_dirs = count_nodes(node)
            files += sub_files
            dirs += sub_dirs + 1
        else:
            files += 1
    return files, dirs
