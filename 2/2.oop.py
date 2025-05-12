import json
from enum import Enum
from typing import Dict, Tuple
from dataclasses import dataclass


class Color(Enum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    DEFAULT = 39
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96


@dataclass
class FontChar:
    pattern: list[str]
    width: int = 0
    height: int = 0

    def __post_init__(self):
        self.height = len(self.pattern)
        if self.height > 0:
            self.width = len(self.pattern[0])


class Printer:
    _font: Dict[str, FontChar] = {}

    def __init__(self, color: Color = Color.DEFAULT,
                 position: Tuple[int, int] = (0, 0),
                 symbol: str = "*"):
        self._color = color
        self._position = position
        self._symbol = symbol
        self._original_position = (0, 0)

    def __enter__(self):
        self._original_position = self._get_cursor_position()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._reset_console()

    @classmethod
    def load_font(cls, font_file: str):
        with open(font_file, 'r', encoding='utf-8') as f:
            font_data = json.load(f)

        cls._font = {}
        for char, pattern in font_data.items():
            cls._font[char] = FontChar(pattern=pattern)

    @classmethod
    def print(cls, text: str, color: Color = Color.DEFAULT,
              position: Tuple[int, int] = (0, 0), symbol: str = "*"):
        printer = cls(color, position, symbol)
        printer._print_text(text)
        printer._reset_console()

    def _print_text(self, text: str):
        if not self._font:
            raise ValueError("Шрифт не загружен. Сначала вызовите Printer.load_font()")

        x, y = self._position
        self._set_cursor_position(x, y)
        self._set_color(self._color)

        output_lines = []
        max_height = max(char.height for char in self._font.values()) if self._font else 0

        for _ in range(max_height):
            output_lines.append("")

        for char in text.upper():
            if char not in self._font:
                continue

            font_char = self._font[char]
            for i in range(font_char.height):
                if i < len(output_lines):
                    line = font_char.pattern[i].replace("*", self._symbol)
                    output_lines[i] += line

        for line in output_lines:
            print(line)
            self._move_cursor_down(1)
            self._move_cursor_left(len(line))

    def _set_color(self, color: Color):
        print(f"\033[{color.value}m", end="")

    def _reset_console(self):
        print("\033[0m", end="")
        self._set_cursor_position(*self._original_position)

    @staticmethod
    def _set_cursor_position(x: int, y: int):
        print(f"\033[{y};{x}H", end="")

    @staticmethod
    def _get_cursor_position() -> Tuple[int, int]:
        return (1, 1)

    @staticmethod
    def _move_cursor_down(lines: int = 1):
        print(f"\033[{lines}B", end="")

    @staticmethod
    def _move_cursor_left(cols: int = 1):
        print(f"\033[{cols}D", end="")


def create_example_font_file(filename: str = "font.json"):
    example_font = {
        "A": [
            "  *  ",
            " * * ",
            "*****",
            "*   *",
            "*   *"
        ],
        "B": [
            "**** ",
            "*   *",
            "**** ",
            "*   *",
            "**** "
        ],
        "C": [
            " ****",
            "*    ",
            "*    ",
            "*    ",
            " ****"
        ],
        " ": [
            "   ",
            "   ",
            "   ",
            "   ",
            "   "
        ],
        "1": [
            " * ",
            "** ",
            " * ",
            " * ",
            "***"
        ],
        "9": [
            "**** ",
            "*   *",
            "**** ",
            "   *",
            "****"
        ],
        "*": [
            " * ",
            "* *",
            " * ",
            "* *",
            " * "
        ]
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(example_font, f, indent=2)


def demo():
    create_example_font_file()
    Printer.load_font("font.json")
    print("\033[2J", end="")
    Printer.print("ABC", Color.BRIGHT_RED, (5, 3), "★")
    Printer.print("1 9", Color.BRIGHT_GREEN, (5, 9), "♦")

    with Printer(Color.BRIGHT_CYAN, (5, 15), "♥") as printer:
        printer._print_text("ABC")
        printer._print_text("1 9")


if __name__ == "__main__":
    demo()
