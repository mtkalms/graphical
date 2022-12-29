from dataclasses import dataclass
from typing import List, Union, Optional, Tuple

from rich.box import Box, HEAVY
from rich.color import Color
from rich.console import Console, ConsoleOptions, RenderResult
from rich.measure import Measurement
from rich.style import Style

from .chart import LabelChartRenderer
from .sparkline import OneLinePlotStyle, Sparkline


@dataclass
class RidgelineRow:
    label: str
    values: List[float]
    color: Union[Color, str] = "default"
    plot_style: Optional[OneLinePlotStyle] = None

    def value_range(self):
        return min(self.values), max(self.values)


class RidgelineChart:
    def __init__(
        self,
        title: str,
        value_range: Optional[Tuple[float, float]] = None,
        color: Union[Color, str] = "default",
        plot_style: OneLinePlotStyle = OneLinePlotStyle.AREA,
        box: Box = HEAVY,
        ticks: Optional[Tuple[float, float]] = None,
    ):
        self.title = title
        self.value_range = value_range
        self.style = Style(color=color)
        self.plot_style = plot_style
        self.box = box
        self.rows: List[RidgelineRow] = []
        self.ticks = ticks

    def add_row(
        self,
        label: str,
        values: List[float],
        color: Union[Color, str] = "default",
        plot_style: Optional[OneLinePlotStyle] = None,
    ) -> RidgelineRow:
        row = RidgelineRow(label, values, color, plot_style)
        self.rows.append(row)
        return row

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        width_graphs = max(len(d.values) for d in self.rows)
        if self.value_range:
            value_range = self.value_range
        else:
            row_min, row_max = zip(*[row.value_range() for row in self.rows])
            value_range = min(row_min), max(row_max)

        chart = LabelChartRenderer(title=self.title, ticks=self.ticks, box=self.box)
        for row in self.rows:
            row_style = Style(color=row.color) if row.color != "default" else self.style
            plot_style = row.plot_style if row.plot_style else self.plot_style
            content = Sparkline(
                values=row.values,
                value_range=value_range,
                color=row_style.color or "default",
                bgcolor=row_style.bgcolor or "default",
                plot_style=plot_style,
                end="",
            )
            chart.add_row(content=content, content_width=width_graphs, label=row.label)
        yield from chart.render()

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        width_labels = max(len(d.label) for d in self.rows) + 1
        width_graphs = max(len(d.values) for d in self.rows)
        width_border = 2
        width = width_labels + width_graphs + width_border
        return Measurement(width, width)


if __name__ == "__main__":
    from rich import print
    from random import randint
    from math import sin, pi

    def wave(r: int) -> int:
        return int(sin((r + randint(0, 3)) * 2 * pi / 25) * 40 - 50)

    for style in OneLinePlotStyle:
        graph = RidgelineChart(
            title=f"Ridgeline Graph Example ({style.name})",
            color="purple",
            plot_style=style,
            ticks=(0, 100),
        )
        for b in range(12):
            data = [wave(d) for d in range(100)]
            graph.add_row(f"row {b}", data)

        print(graph)
        print()
