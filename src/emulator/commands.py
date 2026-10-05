"""Команды эмулятора.

Каждая команда — функция вида ``cmd_имя(shell, args)``.
Она получает эмулятор и список аргументов и возвращает
текст, который нужно показать пользователю.
"""

from emulator.errors import CommandError
from emulator.vfs import count_nodes

MAX_CD_ARGS = 1


def cmd_ls(shell, args):
    """Заглушка ls: вывести имя команды и аргументы."""
    return f"ls {args}"


def cmd_cd(shell, args):
    """Заглушка cd: вывести имя команды и аргументы.

    :raises CommandError: если передано больше одного аргумента.
    """
    if len(args) > MAX_CD_ARGS:
        raise CommandError("cd: слишком много аргументов")
    return f"cd {args}"


def cmd_exit(shell, args):
    """Завершить работу эмулятора.

    :raises CommandError: если переданы аргументы.
    """
    if args:
        raise CommandError("exit: команда не принимает аргументов")
    shell.running = False
    return ""


def cmd_vfs_info(shell, args):
    """Служебная команда: имя VFS и хеш SHA-256 её данных.

    :raises CommandError: если переданы аргументы.
    """
    if args:
        raise CommandError("vfs-info: команда не принимает аргументов")
    files, dirs = count_nodes(shell.vfs.root)
    return (
        f"Имя VFS: {shell.vfs.name}\n"
        f"SHA-256: {shell.vfs.sha256}\n"
        f"Каталогов: {dirs}, файлов: {files}"
    )


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
    "vfs-info": cmd_vfs_info,
}
