from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Union, Optional, List

from rich.box import Box, HEAVY
from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from .cell import PlotCellStyle, PlotCellRenderer
from .chart import LabelChartRenderer

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
            negative_value = self.value <= 0 and cell_range[0] < 0
            negative_range = self.value > 0 > cell_range[0]
            cells += PlotCellRenderer.render(
                self.value,
                value_range=cell_range,
                cell_style=cell_style,
                invert=negative_value or negative_range,
            )
        style = self.style if self.value > 0 else self.style_negative
        yield Segment(cells, style=style)
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
        width: int = WIDTH,
        bar_style: BarStyle = BarStyle.BLOCK,
        box: Box = HEAVY,
    ):
        self.title = title
        self.value_range = value_range
        self.color = color
        self.bgcolor = bgcolor
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
        if self.value_range:
            value_range = 0, self.value_range[1]
        else:
            value_range = 0, max(d.value for d in self.rows)
        width_labels = max(len(d.label) for d in self.rows) + 1
        width_graphs = self.width - width_labels - 2
        chart = LabelChartRenderer(title=self.title, ticks=value_range, box=self.box)
        for row in self.rows:
            content = Bar(
                value=row.value,
                width=width_graphs,
                value_range=value_range,
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
        width: int = WIDTH,
        bar_style: BarStyle = BarStyle.BLOCK,
        box: Box = HEAVY,
    ):
        self.title = title
        self.value_range = value_range
        self.color = color
        self.color_negative = color_negative
        self.bgcolor = bgcolor
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

        if self.value_range:
            max_value = max(abs(d) for d in self.value_range)
        else:
            max_value = max(
                max(d.value for d in self.rows), abs(min(d.value for d in self.rows))
            )
        value_range = -max_value, max_value
        width_labels = max(len(d.label) for d in self.rows) + 1
        width_graphs = self.width - width_labels - 2
        width_graphs -= width_graphs % 2
        chart = LabelChartRenderer(title=self.title, ticks=value_range, box=self.box)
        for row in self.rows:
            content = DivergingBar(
                value=row.value,
                width=width_graphs,
                value_range=value_range,
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
        width: int = WIDTH,
        box: Box = HEAVY,
    ):
        self.title = title
        self.value_range = value_range
        self.colors = colors
        self.bgcolor = bgcolor
        self.width = width
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
        if self.value_range:
            value_range = 0, self.value_range[1]
        else:
            value_range = 0, max(max(d.values) for d in self.rows)
        width_labels = max(len(d.label) for d in self.rows) + 1
        width_graphs = self.width - width_labels - 2
        chart = LabelChartRenderer(title=self.title, ticks=value_range, box=self.box)
        for row in self.rows:
            content = StackedBar(
                values=row.values,
                width=width_graphs,
                value_range=value_range,
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


class DoubleBarChart:
    def __init__(
        self,
        title: str,
        value_range: Optional[Tuple[float, float]] = None,
        colors: List[Union[Color, str]] = "default",
        bgcolor: Union[Color, str] = "default",
        width: int = WIDTH,
        box: Box = HEAVY,
    ):
        self.title = title
        self.value_range = value_range
        self.colors = colors
        self.bgcolor = bgcolor
        self.width = width
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
        if self.value_range:
            value_range = 0, self.value_range[1]
        else:
            value_range = 0, max(max(d.values) for d in self.rows)
        width_labels = max(len(d.label) for d in self.rows) + 1
        width_graphs = self.width - width_labels - 2
        chart = LabelChartRenderer(title=self.title, ticks=value_range, box=self.box)
        for row in self.rows:
            content = DoubleBar(
                values=row.values,
                width=width_graphs,
                value_range=value_range,
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
    import calendar

    from math import sin, pi
    from rich.table import Table

    WIDTH_CONSOLE = 120
    WIDTH_VISUALS = 114

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

    def create_bars(value: float):
        return [
            Bar(
                value=value,
                value_range=(0, 2),
                width=15,
                color="purple",
                bar_style=bar_style,
            )
            for bar_style in BarStyle
        ]

    def create_diverging_bars(value: float):
        return [
            DivergingBar(
                value=value,
                value_range=(-1, 1),
                width=17,
                color="purple",
                color_negative="red",
                bar_style=bar_style,
            )
            for bar_style in BarStyle
        ]

    # Bar Table Example

    console = Console(record=True, width=WIDTH_CONSOLE)
    console.print()
    table = Table(width=WIDTH_CONSOLE - 6)
    table.add_column("")
    for bar_style in BarStyle:
        table.add_column(bar_style.name)
    table.add_column("HALF")
    table.add_row("Bar", *create_bars(1), "")
    table.add_row("", *create_bars(0.5), "")
    table.add_section()
    table.add_row("DivergingBar", *create_diverging_bars(0.5), "")
    table.add_row("", *create_diverging_bars(-0.5), "")
    table.add_section()
    bar = StackedBar(
        values=[3, 2, 1],
        value_range=(0, 10),
        colors=["purple", "red", "yellow"],
        width=17,
    )
    table.add_row("StackedBar", "", "", bar, "", "")
    bar = StackedBar(
        values=[2, 3, 2],
        value_range=(0, 10),
        colors=["purple", "red", "yellow"],
        width=17,
    )
    table.add_row("", "", "", bar, "", "")
    table.add_section()
    bar = DoubleBar(
        values=[3, 2],
        value_range=(0, 4),
        colors=["purple", "red"],
        width=17,
    )
    table.add_row("DoubleBar", "", "", "", "", bar)
    bar = DoubleBar(
        values=[3, 2],
        value_range=(0, 4),
        colors=["purple", "red"],
        width=17,
    )
    table.add_row("", "", "", "", "", bar)

    console.print(table, justify="center")

    # BarChart Example

    console = Console(record=True, width=WIDTH_CONSOLE)
    console.print()
    graph = BarChart(
        title="",
        width=WIDTH_VISUALS,
        value_range=(0, 3),
        color="purple",
    )
    for idx, value in enumerate(wave(12, 0, 0)):
        graph.add_row(label=calendar.month_abbr[idx + 1], value=value + 1)
    console.print(graph, justify="center")
    console.print()

    # DivergingBarChart Example

    console = Console(record=True, width=WIDTH_CONSOLE)
    console.print()
    graph = DivergingBarChart(
        title="",
        width=WIDTH_VISUALS,
        value_range=(-1.5, 1.5),
        color="purple",
        color_negative="red",
    )
    for idx, value in enumerate(wave(12, 1, 0)):
        graph.add_row(label=calendar.month_abbr[idx + 1], value=value + 0.3)
    console.print(graph, justify="center")
    console.print()

    # DivergingBarChart Example

    console = Console(record=True, width=WIDTH_CONSOLE)
    console.print()
    graph = StackedBarChart(
        title="",
        width=WIDTH_VISUALS,
        value_range=(0, 6),
        colors=["purple", "red", "yellow"],
    )
    waves = zip(wave(12, 0, 0), wave(12, 6, 0), wave(12, 3, 0))
    for idx, values in enumerate(waves):
        graph.add_row(
            label=calendar.month_abbr[idx + 1], values=[v + 1 for v in values]
        )
    console.print(graph, justify="center")
    console.print()

    # DivergingBarChart Example

    console = Console(record=True, width=WIDTH_CONSOLE)
    console.print()
    graph = DoubleBarChart(
        title="",
        width=WIDTH_VISUALS,
        value_range=(0, 3),
        colors=["purple", "red"],
    )
    waves = zip(wave(12, 0, 0), wave(12, 6, 0))
    for idx, values in enumerate(waves):
        graph.add_row(
            label=calendar.month_abbr[idx + 1], values=[v + 1 for v in values]
        )
    console.print(graph, justify="center")
    console.print()
