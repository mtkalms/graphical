from rich.console import Console

from graphical.bar import Bar
from graphical.data._bands import bands
from graphical.group import Horizontal, Vertical

from data import data_horizon as data_sets
from graphical.scale.chromatic.sequential import GREENS

levels = 4
colors = GREENS.palette(levels)

value_range = (
    min(d for data in data_sets for d in data),
    max(d for data in data_sets for d in data),
)

graph_rows = []
for data in data_sets:
    horizon_bars = []
    for level, value in bands(data, levels):
        horizon_bars.append(
            Bar(
                value if level < levels else 0.0,
                (0, 1),
                length=9,
                orientation="vertical",
                color=colors[level] if level < levels else None,
                bgcolor=colors[level - 1] if level > 0 else None,
            )
        )
    graph_rows.append(Horizontal(*horizon_bars))
graph = Vertical(*graph_rows, gap=1)

console = Console()
console.print(graph)
