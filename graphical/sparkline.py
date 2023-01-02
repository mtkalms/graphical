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
    from math import sin, pi
    from rich.table import Table

    WIDTH_CONSOLE = 120

    def wave(
        num: int, offset: int = 0, seed: int = 0, scale: float = 1.0
    ) -> List[float]:
        result = [sin(2 * pi * (d + offset) / 10) for d in range(num)]
        if seed > 0:  # overlay second wave
            result = [
                val * sin(2 * pi * d / (40 + seed * 5)) * scale
                for d, val in enumerate(result)
            ]
        return result

    # Sparkline Table Example

    data = wave(22, 0)

    table = Table()
    table.add_column("Plot Style")
    for style in OneLinePlotStyle:
        table.add_column(style.name)
    lines = [
        Sparkline(
            values=data,
            color="purple",
            value_range=(-1.5, 1.5),
            plot_style=style,
        )
        for style in OneLinePlotStyle
    ]
    table.add_row("Sparkline", *lines)

    console = Console(record=True, width=WIDTH_CONSOLE)
    console.print()
    console.print(table, justify="center")
    console.print()
