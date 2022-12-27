import calendar
from math import sin, pi
from typing import List

from rich.console import Console
from rich.table import Table
from rich.terminal_theme import TerminalTheme

from graphical.ridgeline import RidgelineGraph
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


def wave(num: int, offset: int, seed: int = 0, scale: float = 1.0) -> List[float]:
    result = [sin(2 * pi * (d + offset) / 10) for d in range(num)]
    if seed > 0:  # overlay second wave
        result = [
            val * sin(2 * pi * d / (40 + seed * 5)) for d, val in enumerate(result)
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
        Sparkline(data, color="purple", plot_style=style) for style in OneLinePlotStyle
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
    graph = RidgelineGraph(
        title="", color="purple", plot_style=OneLinePlotStyle.AREA, ticks=(0, 100)
    )
    for idx in range(12):
        data = wave(76, idx, idx, 0.8)
        graph.add_row(label=calendar.month_abbr[idx + 1], values=data)
    console.print(graph, justify="center")
    console.print()
    console.save_svg("ridgeline.svg", title="Ridgeline Example", theme=THEME)

    console = Console(record=True, width=WIDTH)
    console.print()
    for style in OneLinePlotStyle:
        graph = RidgelineGraph(
            title=style.name, color="purple", plot_style=style, ticks=(0, 100)
        )
        for idx in range(12):
            data = wave(76, idx, idx)
            graph.add_row(label=calendar.month_abbr[idx + 1], values=data)
        console.print(graph, justify="center")
        console.print()
    console.save_svg(
        "ridgeline-variations.svg", title="Ridgeline Style Examples", theme=THEME
    )
