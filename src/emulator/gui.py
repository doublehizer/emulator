"""Графическое окно эмулятора на tkinter."""

import tkinter as tk
from tkinter import scrolledtext

from emulator.errors import EmulatorError

WINDOW_TITLE = "Эмулятор"
WINDOW_SIZE = "760x480"
PROMPT = "$"
FONT = ("Menlo", 13)
BG_COLOR = "#1e1e1e"
TEXT_COLOR = "#d4d4d4"
COMMAND_COLOR = "#6cb6ff"
ERROR_COLOR = "#ff6b6b"


class EmulatorWindow:
    """Окно эмулятора: поле вывода сверху и строка ввода снизу."""

    def __init__(self, shell):
        """Создать окно для заданного эмулятора.

        :param shell: объект Shell, который выполняет команды.
        """
        self.shell = shell
        self.root = tk.Tk()
        self.root.title(f"{WINDOW_TITLE} — {shell.vfs.name}")
        self.root.geometry(WINDOW_SIZE)
        self.entry = self._create_input()
        self.output = self._create_output()
        self.write(
            f"Эмулятор запущен. VFS: {shell.vfs.name}. "
            "Для выхода введите exit."
        )

    def _create_output(self):
        """Создать поле вывода, доступное только для чтения."""
        output = scrolledtext.ScrolledText(
            self.root, font=FONT, bg=BG_COLOR, fg=TEXT_COLOR,
            state="disabled", wrap="word",
        )
        output.pack(fill="both", expand=True)
        output.tag_config("output", foreground=TEXT_COLOR)
        output.tag_config("command", foreground=COMMAND_COLOR)
        output.tag_config("error", foreground=ERROR_COLOR)
        return output

    def _create_input(self):
        """Создать строку ввода с приглашением слева."""
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(side="bottom", fill="x")
        label = tk.Label(
            frame, text=PROMPT, font=FONT, bg=BG_COLOR, fg=COMMAND_COLOR
        )
        label.pack(side="left")
        entry = tk.Entry(
            frame, font=FONT, bg=BG_COLOR, fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
        )
        entry.pack(side="left", fill="x", expand=True)
        entry.bind("<Return>", self._on_enter)
        entry.focus_set()
        return entry

    def write(self, text, tag="output"):
        """Добавить строку текста в поле вывода.

        :param text: текст для вывода.
        :param tag: стиль текста: output, command или error.
        """
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n", tag)
        self.output.configure(state="disabled")
        self.output.see("end")

    def _on_enter(self, event):
        """Обработать нажатие Enter в строке ввода."""
        line = self.entry.get()
        self.entry.delete(0, "end")
        self.run_line(line)

    def run_line(self, line):
        """Выполнить строку и показать команду и её результат.

        :param line: строка, которую ввёл пользователь.
        :return: True, если команда выполнена без ошибок.
        """
        self.write(f"{PROMPT} {line}", "command")
        try:
            result = self.shell.execute(line)
        except EmulatorError as error:
            self.write(f"Ошибка: {error}", "error")
            return False
        if result:
            self.write(result)
        if not self.shell.running:
            self.root.destroy()
        return True

    def schedule(self, callback, *args):
        """Выполнить функцию сразу после того, как окно откроется.

        :param callback: функция, которую нужно вызвать.
        :param args: аргументы для этой функции.
        """
        self.root.after(0, callback, *args)

    def run(self):
        """Показать окно и ждать действий пользователя."""
        self.root.mainloop()
