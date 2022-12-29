from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Union, Optional, List

from rich.box import Box, HEAVY
from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from graphical.cell import PlotCellStyle, PlotCellRenderer

WIDTH = 50


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


@dataclass
class BarChartRow:
    label: str
    value: float
    color: Union[Color, str] = "default"
    bar_style: Optional[BarStyle] = None


class BarChart:
    def __init__(
        self,
        title: str,
        value_range: Tuple[float, float],
        width: int = WIDTH,
        color: Union[Color, str] = "default",
        bar_style: BarStyle = BarStyle.BLOCK,
        box: Box = HEAVY,
        ticks: Optional[Tuple[float, float]] = None,
    ):
        self.title = title
        self.value_range = value_range
        self.width = width
        self.style = Style(color=color)
        self.bar_style = bar_style
        self.box = box
        self.ticks = ticks
        self.rows: List[BarChartRow] = []

    def add_row(
        self,
        label: str,
        value: float,
        color: Union[Color, str] = "default",
        bar_style: Optional[BarStyle] = None,
    ) -> BarChartRow:
        row = BarChartRow(label, value, color, bar_style)
        self.rows.append(row)
        return row

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        width_labels = max(len(d.label) for d in self.rows) + 1
        width_graphs = self.width - width_labels - 2

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

            yield Segment(f"{row.label : >{width_labels - 1}} ")
            yield Segment(self.box.row_right)

            bar_style = row.bar_style if row.bar_style else self.bar_style
            yield Bar(
                value=row.value,
                width=width_graphs,
                value_range=self.value_range,
                color=row_style.color or "default",
                bgcolor=row_style.bgcolor or "default",
                bar_style=bar_style,
                end="",
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

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, self.width)


if __name__ == "__main__":
    from rich import print
    from random import randint

    for style in BarStyle:
        print(Bar(15.7, (0, 200), color="purple", bar_style=style))

    for style in BarStyle:
        chart = BarChart(
            title="BarChart Example",
            value_range=(0, 100),
            color="purple",
            bar_style=style,
        )
        for idx in range(12):
            chart.add_row(f"idx {idx}", randint(0, 100))
        print(chart)
