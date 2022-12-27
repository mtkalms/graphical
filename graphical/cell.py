import os
from enum import Enum
from typing import Optional, Tuple, List


class PlotCellStyle(Enum):
    AREA_H = (" ▁▂▃▄▅▆▇█", " ", "█", " ▁▁▄▄▄▄██", "██▀▀▀▔▔▔ ")
    AREA_V = (" ▏▎▍▌▋▊▉█", " ", "█", " ▕▕▐▐▐▐██", "██▐▐▐▕▕▕ ")
    LINE_H = (" ▁⎽⎼─⎻⎺▔", " ", " ", None, None)
    LINE_V = ("▏│▕", " ", " ", None, None)
    SHADES = (" ░▒▓█", " ", "█", None, "█▓▒░ ")

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(
        self,
        chars: str,
        under: str,
        over: str,
        matched: Optional[str],
        inverted: Optional[str],
    ):
        self.chars: str = chars
        self.under = under
        self.over = over
        self.matched: str = matched or chars
        self.inverted: str = inverted or chars

    def __rich__(self) -> str:
        return f"{self.name}▕{self.chars}▏▕{self.matched}▏▕{self.inverted}▏ {self.under} {self.over}"


class PlotCellRenderer:
    @staticmethod
    def render(
        value: float,
        value_range: Optional[Tuple[float, float]],
        cell_style: PlotCellStyle = PlotCellStyle.AREA_H,
        invert: bool = False,
        match_inverted: bool = False,
    ) -> str:
        lower, upper = value_range
        if match_inverted and not invert:
            chars = cell_style.matched
        else:
            chars = cell_style.inverted if invert else cell_style.chars
        steps = (upper - lower) / (len(chars) - 1)
        if value < lower:
            return cell_style.over if invert else cell_style.under
        elif value > upper:
            return cell_style.under if invert else cell_style.over
        return chars[int((value - lower) / steps)]


if __name__ == "__main__":
    from rich import print

    for style in PlotCellStyle:
        print(style)
