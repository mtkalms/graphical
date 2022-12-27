import os
from enum import Enum
from typing import Optional, Tuple, List


class PlotCellStyle(Enum):
    AREA_H = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"], " ", "█"
    LINE_H = ["▁", "⎽", "⎼", "─", "⎻", "⎺", "▔"], " ", " "
    AREA_V = ["▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"], " ", "█"
    LINE_V = ["▏", "│", "▕"], " ", " "
    SHADES = [" ", "░", "▒", "▓", "█"], " ", "█"

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, chars: List[str], under: str, over: str):
        self.chars: List[str] = chars
        self.under = under
        self.over = over

    def __rich__(self) -> str:
        return f"{''.join(self.chars)} ({len(self.chars)}) {self.under} {self.over}"


class PlotCellRenderer:
    @staticmethod
    def render(
        value: float,
        value_range: Optional[Tuple[float, float]],
        cell_style: PlotCellStyle = PlotCellStyle.AREA_H,
    ) -> str:
        lower, upper = value_range
        steps = (upper - lower) / (len(cell_style.chars) - 1)
        if value < lower:
            return cell_style.under
        elif value > upper:
            return cell_style.over
        return cell_style.chars[int((value - lower) / steps)]


if __name__ == "__main__":
    from rich import print

    for style in PlotCellStyle:
        print(style)
