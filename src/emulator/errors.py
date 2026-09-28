"""Ошибки эмулятора."""


class EmulatorError(Exception):
    """Общий родитель всех ошибок эмулятора."""


class ParseError(EmulatorError):
    """Строку нельзя разобрать, например не закрыта кавычка."""


class CommandError(EmulatorError):
    """Неизвестная команда или неверные аргументы."""
