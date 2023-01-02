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
        ticks: Optional[Tuple[float, float]] = None,
        plot_style: OneLinePlotStyle = OneLinePlotStyle.AREA,
        box: Box = HEAVY,
    ):
        self.title = title
        self.value_range = value_range
        self.style = Style(color=color)
        self.ticks = ticks
        self.plot_style = plot_style
        self.box = box
        self.rows: List[RidgelineRow] = []

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
    import calendar

    from math import sin, pi

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

    # RidgelineGraph Example

    console = Console(record=True, width=WIDTH_CONSOLE)
    console.print()
    graph = RidgelineChart(
        title="",
        value_range=(-1.5, 1.5),
        color="purple",
        plot_style=OneLinePlotStyle.AREA,
        ticks=(0, 100),
    )
    for idx in range(12):
        data = wave(108, idx, idx, 0.8)
        graph.add_row(label=calendar.month_abbr[idx + 1], values=data)
    console.print(graph, justify="center")
    console.print()

    # RidgelineChart Variations Example

    console = Console(record=True, width=WIDTH_CONSOLE)
    console.print()
    for style in OneLinePlotStyle:
        graph = RidgelineChart(
            title=style.name,
            value_range=(-1.5, 1.5),
            color="purple",
            plot_style=style,
            ticks=(0, 100),
        )
        for idx in range(12):
            data = wave(108, idx, idx)
            graph.add_row(label=calendar.month_abbr[idx + 1], values=data)
        console.print(graph, justify="center")
        console.print()
