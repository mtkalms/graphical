from dataclasses import dataclass
from typing import List, Union, Optional, Tuple

from rich.box import Box, HEAVY
from rich.color import Color
from rich.console import Console, ConsoleOptions, RenderResult
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from graphical.cell import PlotCellRenderer
from graphical.sparkline import OneLinePlotStyle, Sparkline


@dataclass
class RidgelineRow:
    label: str
    values: List[float]
    color: Union[Color, str] = "default"
    plot_style: Optional[OneLinePlotStyle] = None

    def value_range(self):
        return min(self.values), max(self.values)


class RidgelineGraph:

    def __init__(
        self,
        title: str,
        value_range: Optional[Tuple[int, int]] = None,
        color: Union[Color, str] = "default",
        plot_style: OneLinePlotStyle = OneLinePlotStyle.AREA,
        box: Optional[Box] = HEAVY,
        ticks: Optional[Tuple[float, float]] = None
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
        plot_style: Optional[OneLinePlotStyle] = None
    ) -> RidgelineRow:
        row = RidgelineRow(label, values, color, plot_style)
        self.rows.append(row)
        return row

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        width_labels = max(len(d.label) for d in self.rows) + 1
        width_graphs = max(len(d.values) for d in self.rows)
        if self.value_range:
            value_range = self.value_range
        else:
            row_min, row_max = zip(*[row.value_range() for row in self.rows])
            value_range = min(row_min), max(row_max)

        yield Segment(" " * width_labels)
        yield Segment(f"{self.title : ^{width_graphs + 2}}")
        yield Segment("\n")

        yield Segment(" " * width_labels)
        yield Segment(self.box.top_left)
        yield Segment(self.box.top * width_graphs)
        yield Segment(self.box.top_right)
        yield Segment("\n")

        for row in self.rows:
            row_style = Style(color=row.color) if row.color != "default" else self.style

            yield Segment(f"{row.label : >{width_labels - 1 }} ")
            yield Segment(self.box.row_right)

            plot_style = row.plot_style if row.plot_style else self.plot_style
            yield Sparkline(
                values=row.values,
                value_range=value_range,
                color=row_style.color or "default",
                bgcolor=row_style.bgcolor or "default",
                plot_style=plot_style,
                end=""
            )
            yield Segment(self.box.mid_right)
            yield Segment("\n")

        yield Segment(" " * width_labels)
        yield Segment(self.box.bottom_left)
        yield Segment(self.box.bottom * width_graphs)
        yield Segment(self.box.bottom_right)
        yield Segment("\n")

        if self.ticks:
            yield Segment(" " * (width_labels + 1))
            yield Segment(f"{self.ticks[0] : <{width_graphs // 2}}")
            yield Segment(f"{self.ticks[1] : >{width_graphs - width_graphs // 2}}")
            yield Segment("\n")

    def __rich_measure__(self, console: Console, options: ConsoleOptions) -> Measurement:
        width_labels = max(len(d.label) for d in self.rows) + 1
        width_graphs = max(len(d.values) for d in self.rows) + 2
        width = width_labels + width_graphs
        return Measurement(width, width)


if __name__ == '__main__':
    from rich import print
    from random import randint
    from math import sin, pi

    def wave(r: int) -> int:
        return int(sin((r + randint(0, 3)) * 2 * pi / 25) * 40 - 50)

    for style in OneLinePlotStyle:
        print(style.name)
        print()

        graph = RidgelineGraph(
            title="Ridgeline Graph Example",
            color="purple",
            plot_style=style,
            ticks=(0, 100)
        )
        for b in range(12):
            data = [wave(d) for d in range(100)]
            graph.add_row(f"row {b}", data)

        print(graph)
        print()
