from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Union, Optional, List

from rich.box import Box, HEAVY
from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from .chart import LabelChartRenderer
from .cell import PlotCellStyle, PlotCellRenderer

WIDTH = 50


def _stacked(values: List[float]) -> List[float]:
    stacked = []
    for value in values:
        last_value = stacked[-1] if stacked else 0
        stacked.append(value + last_value)
    return stacked


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


class DivergingBar:
    def __init__(
        self,
        value: float,
        value_range: Tuple[float, float],
        width: int = WIDTH,
        color: Union[Color, str] = "default",
        color_negative: Optional[Union[Color, str]] = None,
        bgcolor: Union[Color, str] = "default",
        bar_style: BarStyle = BarStyle.BLOCK,
        end: str = "\n",
    ):
        self.value = value
        self.value_range = value_range
        self.width = width - width % 2
        self.style = Style(color=color, bgcolor=bgcolor)
        self.style_negative = Style(color=color_negative or color, bgcolor=bgcolor)
        self.bar_style = bar_style
        self.end = end

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        max_abs_value = max(abs(d) for d in self.value_range)
        value_range = -max_abs_value, max_abs_value
        cell_style = self.bar_style.horizontal
        step = (value_range[1] * 2) / self.width
        cells = ""
        for idx in range(self.width):
            cell_range = value_range[0] + idx * step, value_range[0] + (idx + 1) * step
            cells += PlotCellRenderer.render(
                self.value,
                value_range=cell_range,
                cell_style=cell_style,
                invert=self.value < 0
                and cell_range[0] < 0
                or self.value > 0 > cell_range[0],
            )
        yield Segment(
            cells, style=self.style if self.value > 0 else self.style_negative
        )
        yield Segment(self.end)

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, self.width)


class StackedBar:
    def __init__(
        self,
        values: List[float],
        value_range: Tuple[float, float],
        colors: List[Union[Color, str]],
        width: int = WIDTH,
        bgcolor: Union[Color, str] = "default",
        end: str = "\n",
    ):
        self.values = values
        self.value_range = value_range
        self.width = width
        self.colors = colors
        self.bgcolor = bgcolor
        self.end = end

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        step = self.value_range[1] / self.width
        values = _stacked(self.values)
        colors = [self.colors[d % len(self.colors)] for d in range(len(values))]
        colors.append(self.bgcolor)
        current = 0
        for idx in range(self.width):
            cell_range = idx * step, (idx + 1) * step
            if values[current] < cell_range[0] and current < len(values) - 1:
                current += 1
            cell = PlotCellRenderer.render(values[current], value_range=cell_range)
            style = Style(color=colors[current], bgcolor=colors[current + 1])
            yield Segment(cell, style)
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

        chart = LabelChartRenderer(title=self.title, ticks=self.ticks, box=self.box)
        for row in self.rows:
            row_style = Style(color=row.color) if row.color != "default" else self.style
            bar_style = row.bar_style if row.bar_style else self.bar_style
            content = Bar(
                value=row.value,
                width=width_graphs,
                value_range=self.value_range,
                color=row_style.color or "default",
                bgcolor=row_style.bgcolor or "default",
                bar_style=bar_style,
                end="",
            )
            chart.add_row(content=content, content_width=width_graphs, label=row.label)
        yield from chart.render()

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, self.width)


if __name__ == "__main__":
    from rich import print
    from random import randint

    print("Bar Example")
    print()
    for style in BarStyle:
        print(Bar(15.7, (0, 200), color="purple", bar_style=style))
    print()

    print("DivergingBar Example")
    print()

    print(DivergingBar(-100, (-200, 200), width=21, color="purple"))
    print(DivergingBar(100, (-200, 200), width=21, color="purple"))
    print()

    print("StackedBar Example")
    print()

    print(StackedBar([50, 20, 10], (0, 200), colors=["red", "yellow", "green"]))
    print()

    for style in BarStyle:
        bar_chart = BarChart(
            title="BarChart Example",
            value_range=(0, 100),
            color="purple",
            bar_style=style,
        )
        for idx in range(12):
            bar_chart.add_row(f"idx {idx}", randint(0, 100))
        print(bar_chart)
        print()
