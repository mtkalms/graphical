from enum import Enum
from typing import Union, List, Optional, Tuple

from rich.color import Color, blend_rgb
from rich.console import ConsoleOptions, RenderResult, Console
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from .cell import PlotCellStyle, PlotCellRenderer


class OneLinePlotStyle(Enum):
    LINE = PlotCellStyle.LINE_V
    AREA = PlotCellStyle.BLOCK_V
    HORIZON = PlotCellStyle.BLOCK_V
    SHADE = PlotCellStyle.SHADE

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, cell_style: PlotCellStyle):
        self.cell_style = cell_style


class Sparkline:
    def __init__(
        self,
        values: List[float],
        value_range: Optional[Tuple[float, float]] = None,
        color: Union[Color, str] = "default",
        bgcolor: Union[Color, str] = "default",
        plot_style: OneLinePlotStyle = OneLinePlotStyle.AREA,
        end: str = "\n",
    ):
        self.values = values
        self.value_range = value_range
        self.style = Style(color=color, bgcolor=bgcolor)
        self.plot_style = plot_style
        self.end = end

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        value_range = self.value_range or (min(self.values), max(self.values))
        cell_style = self.plot_style.cell_style

        if self.plot_style == OneLinePlotStyle.HORIZON:
            lower, upper = value_range
            mid = lower + (upper - lower) / 2
            mid_shade = Color.from_triplet(
                blend_rgb(
                    self.style.bgcolor.get_truecolor(),
                    self.style.color.get_truecolor(),
                    0.5,
                )
            )
            lower_style = Style(bgcolor=self.style.bgcolor, color=mid_shade)
            upper_style = Style(bgcolor=mid_shade, color=self.style.color)
            for value in self.values:
                cell = PlotCellRenderer.render(
                    value=value,
                    value_range=(lower, mid) if value < mid else (mid, upper),
                    cell_style=cell_style,
                )
                yield Segment(cell, style=lower_style if value < mid else upper_style)
        else:
            cells = ""
            for value in self.values:
                cells += PlotCellRenderer.render(
                    value=value, value_range=value_range, cell_style=cell_style
                )
            yield Segment(cells, self.style)
        yield Segment(self.end)

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        width = len(self.values)
        return Measurement(width, width)


if __name__ == "__main__":
    from rich import print
    from rich.table import Table
    from random import randint
    from math import sin, pi

    for style in OneLinePlotStyle:
        print(f"Sparkline Examples ({style.name})")
        print()

        data = [randint(0, 100) for d in range(100)]
        line = Sparkline(data, color="cyan", plot_style=style)
        print(line)
        print()

        data = [sin(2 * pi * d / 10) for d in range(100)]
        line = Sparkline(data, value_range=(0, 2), color="purple", plot_style=style)
        print(line)
        print()

    for style in OneLinePlotStyle:
        data = [sin(2 * pi * d / 10) for d in range(50)]
        line = Sparkline(data, color="purple", plot_style=style)

        table = Table(
            title=f"Sparkline Table Example ({style.name})", show_header=False
        )
        table.add_row("row 0", line)
        table.add_row("row 1", line)
        table.add_row("row 2", line)
        print(table)
