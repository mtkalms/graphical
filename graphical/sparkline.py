from enum import Enum
from typing import Union, List, Optional, Tuple

from rich.color import Color
from rich.console import ConsoleOptions, RenderResult, Console
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from graphical.cell import PlotCellStyle, PlotCellRenderer


class OneLinePlotStyle(Enum):
    LINE = PlotCellStyle.LINE
    AREA = PlotCellStyle.AREA

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
        plot_style: OneLinePlotStyle = OneLinePlotStyle.AREA
    ):
        self.values = values
        self.value_range = value_range if value_range else (min(values), max(values))
        self.style = Style(color=color, bgcolor=bgcolor)
        self.plot_style = plot_style

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        cells = ""
        for value in self.values:
            cells += PlotCellRenderer.render(
                value=value,
                value_range=self.value_range,
                cell_style=self.plot_style.cell_style
            )
        yield Segment(cells, self.style)
        yield Segment("\n")

    def __rich_measure__(self, console: Console, options: ConsoleOptions) -> Measurement:
        width = len(self.values)
        return Measurement(width, width)


if __name__ == '__main__':
    from rich import print
    from rich.table import Table
    from random import randint
    from math import sin, pi

    for style in OneLinePlotStyle:
        print(style.name)
        print()

        data = [randint(0, 100) for d in range(100)]
        line = Sparkline(data, color="blue", plot_style=style)
        print(line)
        print()

        data = [sin(2 * pi * d / 10) for d in range(100)]
        line = Sparkline(data, value_range=(0, 2), color="purple", plot_style=style)
        print(line)
        print()

        data = [sin(2 * pi * d / 10) for d in range(20)]
        line = Sparkline(data, color="purple", plot_style=style)

        table = Table(
            title="Sparkline Table Example",
            show_header=False
        )
        table.add_row("row 0", line)
        table.add_row("row 1", line)
        table.add_row("row 2", line)
        print(table)
