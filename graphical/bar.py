from enum import Enum
from typing import Tuple, Union

from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from graphical.cell import PlotCellStyle, PlotCellRenderer

WIDTH = 150


class BarStyle(Enum):
    LIGHT = PlotCellStyle.BAR_LIGHT_H, PlotCellStyle.BAR_LIGHT_V
    HEAVY = PlotCellStyle.BAR_HEAVY_H, PlotCellStyle.BAR_HEAVY_V
    BLOCK = PlotCellStyle.BLOCK_H, PlotCellStyle.BLOCK_V
    SHADE = PlotCellStyle.SHADE, PlotCellStyle.SHADE

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, horizontal: PlotCellStyle, vertical: PlotCellStyle):
        self.horizontal = horizontal
        self.vertical = vertical


class Bar:
    def __init__(
        self,
        value: float,
        value_range: Tuple[float, float],
        width: int = WIDTH,
        color: Union[Color, str] = "default",
        bgcolor: Union[Color, str] = "default",
        bar_style: BarStyle = BarStyle.BLOCK,
        end: str = "\n",
    ):
        self.value = value
        self.value_range = value_range
        self.width = width
        self.style = Style(color=color, bgcolor=bgcolor)
        self.bar_style = bar_style
        self.end = end

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        cell_style = self.bar_style.horizontal
        step = self.value_range[1] / self.width
        cells = ""
        for idx in range(self.width):
            cell_range = idx * step, (idx + 1) * step
            cells += PlotCellRenderer.render(
                self.value, value_range=cell_range, cell_style=cell_style
            )
        yield Segment(cells, style=self.style)
        yield Segment(self.end)

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, self.width)


if __name__ == "__main__":
    from rich import print

    for style in BarStyle:
        print(Bar(15.7, (0, 200), color="purple", bar_style=style))
