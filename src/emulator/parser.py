"""Разбор строки, введённой пользователем, на команду и аргументы."""

import shlex

from emulator.errors import ParseError

SHLEX_MESSAGES = {
    "No closing quotation": "не закрыта кавычка",
    "No escaped character": "после \\ нет символа",
}


def parse_line(line):
    """Разделить строку на имя команды и список аргументов.

    Учитывает кавычки: строка ``ls "My Docs"`` даёт один
    аргумент ``My Docs``, а не два.

    :param line: строка, которую ввёл пользователь.
    :return: кортеж ``(команда, аргументы)``.
        Для пустой строки возвращается ``(None, [])``.
    :raises ParseError: если строку нельзя разобрать.
    """
    try:
        tokens = shlex.split(line)
    except ValueError as error:
        message = SHLEX_MESSAGES.get(str(error), str(error))
        raise ParseError(f"синтаксическая ошибка: {message}") from error
    if not tokens:
        return None, []
    return tokens[0], tokens[1:]
