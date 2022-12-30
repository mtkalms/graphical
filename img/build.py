import calendar
from math import sin, pi
from typing import List

from rich.console import Console
from rich.table import Table
from rich.terminal_theme import TerminalTheme

from graphical.bar import (
    Bar,
    BarStyle,
    BarChart,
    DivergingBar,
    StackedBar,
    DoubleBar,
    DivergingBarChart,
    StackedBarChart,
    DoubleBarChart,
)
from graphical.ridgeline import RidgelineChart
from graphical.sparkline import OneLinePlotStyle, Sparkline

WIDTH = 90
THEME = TerminalTheme(
    background=(41, 45, 62),
    foreground=(149, 157, 203),
    normal=[
        (41, 45, 62),
        (240, 113, 120),
        (195, 232, 141),
        (255, 203, 107),
        (130, 170, 255),
        (199, 146, 234),
        (137, 221, 255),
        (149, 157, 203),
    ],
)


def wave(num: int, offset: int = 0, seed: int = 0, scale: float = 1.0) -> List[float]:
    result = [sin(2 * pi * (d + offset) / 10) for d in range(num)]
    if seed > 0:  # overlay second wave
        result = [
            val * sin(2 * pi * d / (40 + seed * 5)) * scale
            for d, val in enumerate(result)
        ]
    return result


if __name__ == "__main__":

    # Sparkline Table Example

    data = wave(14, 0)

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

    console = Console(record=True, width=WIDTH)
    console.print()
    console.print(table, justify="center")
    console.print()
    console.save_svg(
        "sparkline-table.svg", title="Sparkline Table Example", theme=THEME
    )

    # RidgelineGraph Example

    console = Console(record=True, width=WIDTH)
    console.print()
    graph = RidgelineChart(
        title="",
        value_range=(-1.5, 1.5),
        color="purple",
        plot_style=OneLinePlotStyle.AREA,
        ticks=(0, 100),
    )
    for idx in range(12):
        data = wave(76, idx, idx, 0.8)
        graph.add_row(label=calendar.month_abbr[idx + 1], values=data)
    console.print(graph, justify="center")
    console.print()
    console.save_svg("ridgeline.svg", title="RidgelineChart Example", theme=THEME)

    # RidgelineChart Variations Example

    console = Console(record=True, width=WIDTH)
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
            data = wave(76, idx, idx)
            graph.add_row(label=calendar.month_abbr[idx + 1], values=data)
        console.print(graph, justify="center")
        console.print()
    console.save_svg(
        "ridgeline-variations.svg", title="RidgelineChart Style Examples", theme=THEME
    )

    # Bar Table Example

    def create_bars(value: float):
        return [
            Bar(
                value=value,
                value_range=(0, 2),
                width=10,
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
                width=10,
                color="purple",
                color_negative="red",
                bar_style=bar_style,
            )
            for bar_style in BarStyle
        ]

    console = Console(record=True, width=WIDTH)
    console.print()
    table = Table(width=82)
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
        width=10,
    )
    table.add_row("StackedBar", "", "", bar, "", "")
    bar = StackedBar(
        values=[2, 3, 2],
        value_range=(0, 10),
        colors=["purple", "red", "yellow"],
        width=10,
    )
    table.add_row("", "", "", bar, "", "")
    table.add_section()
    bar = DoubleBar(
        values=[3, 2],
        value_range=(0, 4),
        colors=["purple", "red"],
        width=10,
    )
    table.add_row("DoubleBar", "", "", "", "", bar)
    bar = DoubleBar(
        values=[3, 2],
        value_range=(0, 4),
        colors=["purple", "red"],
        width=10,
    )
    table.add_row("", "", "", "", "", bar)

    console.print(table, justify="center")
    console.save_svg("bar-table.svg", title="Bar Table Example", theme=THEME)

    # BarChart Example

    console = Console(record=True, width=WIDTH)
    console.print()
    graph = BarChart(
        title="",
        width=83,
        value_range=(0, 3),
        color="purple",
        ticks=(0, 3.0),
    )
    for idx, value in enumerate(wave(12, 0, 0)):
        graph.add_row(label=calendar.month_abbr[idx + 1], value=value + 1)
    console.print(graph, justify="center")
    console.print()
    console.save_svg("barchart.svg", title="BarChart Example", theme=THEME)

    # DivergingBarChart Example

    console = Console(record=True, width=WIDTH)
    console.print()
    graph = DivergingBarChart(
        title="",
        width=83,
        value_range=(-1.5, 1.5),
        color="purple",
        color_negative="red",
        ticks=(-1.5, 1.5),
    )
    for idx, value in enumerate(wave(12, 1, 0)):
        graph.add_row(label=calendar.month_abbr[idx + 1], value=value + 0.3)
    console.print(graph, justify="center")
    console.print()
    console.save_svg(
        "diverging-barchart.svg", title="DivergingBarChart Example", theme=THEME
    )

    # DivergingBarChart Example

    console = Console(record=True, width=WIDTH)
    console.print()
    graph = StackedBarChart(
        title="",
        width=83,
        value_range=(0, 6),
        colors=["purple", "red", "yellow"],
        ticks=(0, 6.0),
    )
    waves = zip(wave(12, 0, 0), wave(12, 6, 0), wave(12, 3, 0))
    for idx, values in enumerate(waves):
        graph.add_row(
            label=calendar.month_abbr[idx + 1], values=[v + 1 for v in values]
        )
    console.print(graph, justify="center")
    console.print()
    console.save_svg(
        "stacked-barchart.svg", title="StackedBarChart Example", theme=THEME
    )

    # DivergingBarChart Example

    console = Console(record=True, width=WIDTH)
    console.print()
    graph = DoubleBarChart(
        title="",
        width=83,
        value_range=(0, 3),
        colors=["purple", "red"],
        ticks=(0, 3.0),
    )
    waves = zip(wave(12, 0, 0), wave(12, 6, 0))
    for idx, values in enumerate(waves):
        graph.add_row(
            label=calendar.month_abbr[idx + 1], values=[v + 1 for v in values]
        )
    console.print(graph, justify="center")
    console.print()
    console.save_svg("double-barchart.svg", title="DoubleBarChart Example", theme=THEME)
