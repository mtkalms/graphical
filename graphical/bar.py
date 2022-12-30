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
        last_value = 0 if not stacked else stacked[-1]
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
        color: Union[Color, str] = "default",
        bgcolor: Union[Color, str] = "default",
        width: int = WIDTH,
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
        color: Union[Color, str] = "default",
        color_negative: Optional[Union[Color, str]] = None,
        bgcolor: Union[Color, str] = "default",
        width: int = WIDTH,
        bar_style: BarStyle = BarStyle.BLOCK,
        end: str = "\n",
    ):
        self.value = value
        self.value_range = value_range
        self.style = Style(color=color, bgcolor=bgcolor)
        self.style_negative = Style(color=color_negative or color, bgcolor=bgcolor)
        self.width = width - width % 2
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
        bgcolor: Union[Color, str] = "default",
        width: int = WIDTH,
        end: str = "\n",
    ):
        self.values = values
        self.value_range = value_range
        self.colors = colors
        self.bgcolor = bgcolor
        self.width = width
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


class DoubleBar:
    def __init__(
        self,
        values: List[float],
        value_range: Tuple[float, float],
        colors: List[Union[Color, str]],
        bgcolor: Union[Color, str] = "default",
        width: int = WIDTH,
        end: str = "\n",
    ):
        self.values = values
        self.value_range = value_range
        self.colors = colors
        self.bgcolor = bgcolor
        self.width = width
        self.end = end

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        step = self.value_range[1] / self.width
        for idx in range(self.width):
            cell_range = idx * step, (idx + 1) * step
            first_lower = self.values[0] > cell_range[1]
            first_match = cell_range[0] < self.values[0] < cell_range[1]
            second_lower = self.values[1] > cell_range[1]
            second_match = cell_range[0] < self.values[1] < cell_range[1]
            if first_lower or first_match:
                color = self.colors[0]
                cell = "▀"
                if second_lower or second_match:
                    bgcolor = self.colors[1]
                else:
                    bgcolor = self.bgcolor
            else:
                color = self.colors[1]
                bgcolor = self.bgcolor
                if second_lower or second_match:
                    cell = "▄"
                else:
                    cell = " "
            style = Style(color=color, bgcolor=bgcolor)
            yield Segment(cell, style=style)
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
    bgcolor: Union[Color, str] = "default"
    bar_style: Optional[BarStyle] = None


@dataclass
class MultiBarChartRow:
    label: str
    values: List[float]
    colors: List[Union[Color, str]] = None
    bgcolor: Union[Color, str] = "default"
    bar_style: Optional[BarStyle] = None


class BarChart:
    def __init__(
        self,
        title: str,
        value_range: Tuple[float, float],
        color: Union[Color, str] = "default",
        bgcolor: Union[Color, str] = "default",
        ticks: Optional[Tuple[float, float]] = None,
        width: int = WIDTH,
        bar_style: BarStyle = BarStyle.BLOCK,
        box: Box = HEAVY,
    ):
        self.title = title
        self.value_range = value_range
        self.color = color
        self.bgcolor = bgcolor
        self.ticks = ticks
        self.width = width
        self.bar_style = bar_style
        self.box = box
        self.rows: List[BarChartRow] = []

    def add_row(
        self,
        label: str,
        value: float,
        color: Optional[Union[Color, str]] = None,
        bgcolor: Optional[Union[Color, str]] = None,
        bar_style: Optional[BarStyle] = None,
    ) -> BarChartRow:
        row = BarChartRow(
            label=label,
            value=value,
            color=color,
            bgcolor=bgcolor,
            bar_style=bar_style,
        )
        self.rows.append(row)
        return row

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        width_labels = max(len(d.label) for d in self.rows) + 1
        width_graphs = self.width - width_labels - 2
        chart = LabelChartRenderer(title=self.title, ticks=self.ticks, box=self.box)
        for row in self.rows:
            content = Bar(
                value=row.value,
                width=width_graphs,
                value_range=self.value_range,
                color=row.color or self.color,
                bgcolor=row.bgcolor or self.bgcolor,
                bar_style=row.bar_style or self.bar_style,
                end="",
            )
            chart.add_row(content=content, content_width=width_graphs, label=row.label)
        yield from chart.render()

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, self.width)


class DivergingBarChart:
    def __init__(
        self,
        title: str,
        value_range: Tuple[float, float],
        color: Union[Color, str] = "default",
        color_negative: Optional[Union[Color, str]] = None,
        bgcolor: Union[Color, str] = "default",
        ticks: Optional[Tuple[float, float]] = None,
        width: int = WIDTH,
        bar_style: BarStyle = BarStyle.BLOCK,
        box: Box = HEAVY,
    ):
        self.title = title
        self.value_range = value_range
        self.color = color
        self.color_negative = color_negative
        self.bgcolor = bgcolor
        self.ticks = ticks
        self.width = width
        self.bar_style = bar_style
        self.box = box
        self.rows: List[BarChartRow] = []

    def add_row(
        self,
        label: str,
        value: float,
        bgcolor: Optional[Union[Color, str]] = None,
        bar_style: Optional[BarStyle] = None,
    ) -> BarChartRow:
        row = BarChartRow(
            label=label,
            value=value,
            bgcolor=bgcolor,
            bar_style=bar_style,
        )
        self.rows.append(row)
        return row

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        width_labels = max(len(d.label) for d in self.rows) + 1
        width_graphs = self.width - width_labels - 2
        width_graphs -= width_graphs % 2
        chart = LabelChartRenderer(title=self.title, ticks=self.ticks, box=self.box)
        for row in self.rows:
            content = DivergingBar(
                value=row.value,
                width=width_graphs,
                value_range=self.value_range,
                color=self.color,
                color_negative=self.color_negative,
                bgcolor=row.bgcolor or self.bgcolor,
                bar_style=row.bar_style or self.bar_style,
                end="",
            )
            chart.add_row(content=content, content_width=width_graphs, label=row.label)
        yield from chart.render()

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, self.width)


class StackedBarChart:
    def __init__(
        self,
        title: str,
        value_range: Tuple[float, float],
        colors: List[Union[Color, str]] = "default",
        bgcolor: Union[Color, str] = "default",
        ticks: Optional[Tuple[float, float]] = None,
        width: int = WIDTH,
        bar_style: BarStyle = BarStyle.BLOCK,
        box: Box = HEAVY,
    ):
        self.title = title
        self.value_range = value_range
        self.colors = colors
        self.bgcolor = bgcolor
        self.ticks = ticks
        self.width = width
        self.bar_style = bar_style
        self.box = box
        self.rows: List[MultiBarChartRow] = []

    def add_row(
        self,
        label: str,
        values: List[float],
        bgcolor: Optional[Union[Color, str]] = None,
    ) -> MultiBarChartRow:
        row = MultiBarChartRow(
            label=label,
            values=values,
            bgcolor=bgcolor,
        )
        self.rows.append(row)
        return row

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        width_labels = max(len(d.label) for d in self.rows) + 1
        width_graphs = self.width - width_labels - 2
        chart = LabelChartRenderer(title=self.title, ticks=self.ticks, box=self.box)
        for row in self.rows:
            content = StackedBar(
                values=row.values,
                width=width_graphs,
                value_range=self.value_range,
                colors=row.colors or self.colors,
                bgcolor=row.bgcolor or self.bgcolor,
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
    for current_style in BarStyle:
        print(Bar(15.7, (0, 200), color="purple", bar_style=current_style))
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

    print("StackedBar Example")
    print()
    print(DoubleBar([50, 20], (0, 200), colors=["purple", "red"]))
    print()

    bar_chart = BarChart(title="BarChart Example", value_range=(0, 100), color="purple")
    for row_idx in range(6):
        current_row = bar_chart.add_row(f"idx {row_idx}", randint(0, 100))
        if row_idx == 3:
            current_row.bgcolor = "white"
    print(bar_chart)
    print()

    bar_chart = DivergingBarChart(
        title="Diverging Example",
        value_range=(-100, 100),
        color="purple",
        color_negative="red",
    )
    for row_idx in range(6):
        current_row = bar_chart.add_row(f"idx {row_idx}", randint(-100, 100))
        if row_idx == 3:
            current_row.bgcolor = "white"
    print(bar_chart)
    print()

    bar_chart = StackedBarChart(
        title="Diverging Example",
        value_range=(0, 100),
        colors=["purple", "red", "yellow"],
    )
    for row_idx in range(6):
        current_row = bar_chart.add_row(
            f"idx {row_idx}", [randint(0, 33) for _ in range(3)]
        )
        if row_idx == 3:
            current_row.bgcolor = "white"
    print(bar_chart)
    print()
