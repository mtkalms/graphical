import calendar
from math import sin, pi
from pathlib import Path
from typing import List
from rich.table import Table
from rich.console import Console
from rich.box import SIMPLE
from rich.terminal_theme import TerminalTheme

from graphical.bar import Bar, BarChart, BarStyle, DivergingBar, DivergingBarChart, DoubleBar, DoubleBarChart, StackedBar, StackedBarChart
from graphical.ridgeline import RidgelineChart
from graphical.sparkline import OneLinePlotStyle, Sparkline


IMG_PATH = Path(__file__).resolve().parent.parent/'img'
WIDTH_CONSOLE = 120
WIDTH_VISUALS = 114
FAR = 0.6525
CODE_FORMAT = """\
<svg class="rich-terminal" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <!-- Generated with Rich https://www.textualize.io -->
    
    <style>
    .{unique_id}-matrix {{
        font-family: Courier New;
        font-size: 24px;
        line-height: 18px;
        font-variant-east-asian: full-width;
    }}
    {styles}
    </style>
    <defs>
    <clipPath id="{unique_id}-clip-terminal">
      <rect x="0" y="0" width="{terminal_width}" height="{terminal_height}" />
    </clipPath>
    {lines}
    </defs>
    <g transform="translate({terminal_x}, {terminal_y})" clip-path="url(#{unique_id}-clip-terminal)">
    {backgrounds}
    <g class="{unique_id}-matrix">
    {matrix}
    </g>
    </g>
</svg>
"""
THEME = TerminalTheme(
    (0, 0, 0),
    (128, 128, 128),
    [
        (75, 78, 85),
        (236, 58, 55),
        (58, 217, 0),
        (250,208,0),
        (96, 138, 177),
        (152, 114, 159),
        (104, 160, 179),
        (197, 200, 198),
        (154, 155, 153),
    ]
)

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


def sparkline_variations():
    table = Table(
        box=SIMPLE, 
        show_header=False, 
        show_lines=True
    )
    for d, style in enumerate(OneLinePlotStyle):
        table.add_row(
            style.name,
            Sparkline(
                values=wave(108, 5, 5),
                color="purple",
                value_range=(-1.5, 1.5),
                plot_style=style,
            )
        )
    console = Console(record=True, width=WIDTH_CONSOLE)
    console.print(table, justify="center")
    console.save_svg(IMG_PATH/'sparkline.svg', code_format=CODE_FORMAT, font_aspect_ratio=FAR, theme=THEME)


def rigdeline_example():
    console = Console(record=True, width=WIDTH_CONSOLE)
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
    console.save_svg(IMG_PATH/'ridgeline.svg', code_format=CODE_FORMAT, font_aspect_ratio=FAR, theme=THEME)


def rigdeline_variations():
    console = Console(record=True, width=WIDTH_CONSOLE)
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
    console.save_svg(IMG_PATH/'ridgeline-variations.svg', code_format=CODE_FORMAT, font_aspect_ratio=FAR, theme=THEME)


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


def bar_variations():
    console = Console(record=True, width=WIDTH_CONSOLE)
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
    console.save_svg(IMG_PATH/'bar-variations.svg', code_format=CODE_FORMAT, font_aspect_ratio=FAR, theme=THEME)


def bar_example():
    console = Console(record=True, width=WIDTH_CONSOLE)
    graph = BarChart(
        title="",
        width=WIDTH_VISUALS,
        value_range=(0, 3),
        color="purple",
    )
    for idx, value in enumerate(wave(12, 0, 0)):
        graph.add_row(label=calendar.month_abbr[idx + 1], value=value + 1)
    console.print(graph, justify="center")
    console.save_svg(IMG_PATH/'bar.svg', code_format=CODE_FORMAT, font_aspect_ratio=FAR, theme=THEME)


def bar_diverging_example():
    console = Console(record=True, width=WIDTH_CONSOLE)
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
    console.save_svg(IMG_PATH/'bar-diverging.svg', code_format=CODE_FORMAT, font_aspect_ratio=FAR, theme=THEME)

def bar_stacked_example():
    console = Console(record=True, width=WIDTH_CONSOLE)
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
    console.save_svg(IMG_PATH/'bar-stacked.svg', code_format=CODE_FORMAT, font_aspect_ratio=FAR, theme=THEME)


def bar_double_example():
    console = Console(record=True, width=WIDTH_CONSOLE)
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
    console.save_svg(IMG_PATH/'bar-double.svg', code_format=CODE_FORMAT, font_aspect_ratio=FAR, theme=THEME)


if __name__ == "__main__":
    sparkline_variations()
    rigdeline_example()
    rigdeline_variations()
    bar_example()
    bar_variations()
    bar_diverging_example()
    bar_stacked_example()
    bar_double_example()
