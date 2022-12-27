import os
from enum import Enum
from typing import Optional, Tuple, List


class PlotCellStyle(Enum):
    AREA_H = (
        [" ", "▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"],
        ["█", "█", "▀", "▀", "▀", "▔", "▔", "▔", " "],
        " ",
        "█",
    )
    AREA_V = (
        [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"],
        ["█", "█", "▐", "▐", "▐", "▕", "▕", "▕", " "],
        " ",
        "█",
    )
    LINE_H = (
        [" ", "▁", "⎽", "⎼", "─", "⎻", "⎺", "▔"],
        None,
        " ",
        " ",
    )
    LINE_V = (
        ["▏", "│", "▕"],
        None,
        " ",
        " ",
    )
    SHADES = (
        [" ", "░", "▒", "▓", "█"],
        ["█", "▓", "▒", "░", " "],
        " ",
        "█",
    )

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(
        self, chars: List[str], inverted: Optional[List[str]], under: str, over: str
    ):
        self.chars: List[str] = chars
        self.inverted: List[str] = inverted or chars
        self.under = under
        self.over = over

    def __rich__(self) -> str:
        return f"▕{''.join(self.chars)}▏({len(self.chars)})▕{''.join(self.inverted)}▏{self.under} {self.over}"


class PlotCellRenderer:
    @staticmethod
    def render(
        value: float,
        value_range: Optional[Tuple[float, float]],
        cell_style: PlotCellStyle = PlotCellStyle.AREA_H,
        invert: bool = False,
    ) -> str:
        lower, upper = value_range
        chars = cell_style.inverted if invert else cell_style.chars
        steps = (upper - lower) / (len(chars) - 1)
        if value < lower:
            return cell_style.under
        elif value > upper:
            return cell_style.over
        return chars[int((value - lower) / steps)]


if __name__ == "__main__":
    from rich import print

    for style in PlotCellStyle:
        print(style)
