import calendar
import random
from math import sin, pi
from typing import List

from rich.console import Console
from rich.table import Table
from rich.terminal_theme import TerminalTheme

from graphical.bar import Bar, BarStyle, BarChart
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

    def create_bars():
        return [
            Bar(
                value=random.randint(0, 100),
                value_range=(0, 100),
                width=16,
                color="purple",
                bar_style=bar_style,
            )
            for bar_style in BarStyle
        ]

    console = Console(record=True, width=WIDTH)
    console.print()
    table = Table(width=82)
    table.add_column()
    for bar_style in BarStyle:
        table.add_column(bar_style.name)
    for idx in range(12):
        table.add_row(calendar.month_abbr[idx + 1], *create_bars())
    console.print(table, justify="center")
    console.save_svg("bar-table.svg", title="Bar Table Example", theme=THEME)

    # BarChart Example

    console = Console(record=True, width=WIDTH)
    console.print()
    graph = BarChart(
        title="",
        width=83,
        value_range=(0, 2),
        color="purple",
        ticks=(0, 2.0),
    )
    for idx, value in enumerate(wave(12, 0, 0)):
        graph.add_row(label=calendar.month_abbr[idx + 1], value=value + 1)
    console.print(graph, justify="center")
    console.print()
    console.save_svg("barchart.svg", title="BarChart Example", theme=THEME)

    # BarChart Variations Example

    console = Console(record=True, width=WIDTH)
    console.print()
    for style in BarStyle:
        graph = BarChart(
            title=style.name,
            width=83,
            value_range=(0, 2),
            color="purple",
            bar_style=style,
            ticks=(0, 2.0),
        )
        for idx, value in enumerate(wave(12, 0, 0)):
            graph.add_row(label=calendar.month_abbr[idx + 1], value=value + 1)
        console.print(graph, justify="center")
        console.print()
    console.save_svg(
        "barchart-variations.svg", title="BarChart Style Examples", theme=THEME
    )
