from enum import Enum
from typing import Optional, Tuple


class PlotCellStyle(Enum):
    """Cell styles for plot charts.

    Args:
        chars (str): String of chars for values in ascending order.
        under (str): Char for value ranges under the value.
        over (str): Char for value ranges over the value.
        matched (str): String of chars for values in ascending order matching the length of inverted. Reverts to chars.
        inverted (str): String of chars for values in descending order. Reverts to chars.
    """

    BLOCK_H = (" ▏▎▍▌▋▊▉█", " ", "█", " ▕▕▐▐▐▐██", "██▐▐▐▕▕▕ ")
    """Cell for horizontal area or full-width bar plots."""
    BLOCK_V = (" ▁▂▃▄▅▆▇█", " ", "█", " ▁▁▄▄▄▄██", "██▀▀▀▔▔▔ ")
    """Cell for vertical area or full-width bar plots."""
    BAR_LIGHT_H = (" ╴─", " ", "─", None, "─╶ ")
    """Cell for horizontal light bar plots."""
    BAR_LIGHT_V = (" ╷│", " ", "│", None, "│╵ ")
    """Cell for vertical light bar plots."""
    BAR_HEAVY_H = (" ╸━", " ", "━", None, "━╺ ")
    """Cell for horizontal heavy bar plots."""
    BAR_HEAVY_V = (" ╻┃", " ", "┃", None, "┃╹ ")
    """Cell for vertical heavy bar plots."""
    LINE_H = ("▏│▕", " ", " ", None, None)
    """Cell for horizontal line plots."""
    LINE_V = (" ▁⎽⎼─⎻⎺▔", " ", " ", None, None)
    """Cell for vertical line plots."""
    SHADE = (" ░▒▓█", " ", "█", None, "█▓▒░ ")
    """Cell for shading."""

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
    """Renderer for plot cells."""

    @staticmethod
    def render(
        value: float,
        value_range: Optional[Tuple[float, float]],
        cell_style: PlotCellStyle,
        invert: bool = False,
        match_inverted: bool = False,
    ) -> str:
        """Render plot cell.

        Args:
            value (float): Value of the cell.
            value_range (Tuple[float, float], optional): Value range of the cell.
            cell_style (PlotCellStyle): Data representation syle..
            invert (bool): Invert cell direction. Defaults to False.
            match_inverted (bool): Use limited resolution to match inverted cells. Defaults to False.

        Returns:
            str: Char for plot cell.
        """
        lower, upper = value_range
        if match_inverted and not invert:
            chars = cell_style.matched
        else:
            chars = cell_style.inverted if invert else cell_style.chars
        if value < lower:
            return cell_style.over if invert else cell_style.under
        elif value > upper:
            return cell_style.under if invert else cell_style.over
        steps = (upper - lower) / (len(chars) - 1)
        return chars[int(round((value - lower) / steps))]


if __name__ == "__main__":
    from rich import print

    for style in PlotCellStyle:
        print(style)
