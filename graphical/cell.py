from enum import Enum
from typing import Optional, Tuple, List


class PlotCellStyle(Enum):
    AREA = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"], " ", "█"
    LINE = ["▁", "⎽", "⎼", "─", "⎻", "⎺", "▔", "▔"], " ", " "

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, chars: List[str], under: str, over: str):
        self.chars: List[str] = chars
        self.under = under
        self.over = over


class PlotCellRenderer:
    @staticmethod
    def render(
        value: float,
        value_range: Optional[Tuple[float, float]],
        cell_style: PlotCellStyle = PlotCellStyle.AREA,
    ) -> str:
        lower, upper = value_range
        steps = (upper - lower) / (len(cell_style.chars) - 1)
        if value < lower:
            return cell_style.under
        elif value > upper:
            return cell_style.over
        return cell_style.chars[int((value - lower) / steps)]
