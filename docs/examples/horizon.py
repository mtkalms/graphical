from rich.console import Console

from graphical.bar import Bar
from graphical.group import Horizontal, Vertical

from data import data_horizon as data_sets
from graphical.scale.chromatic.sequential import GREENS

colors = GREENS.palette(5)
levels = 4

value_range = [
    min(d for data in data_sets for d in data),
    max(d for data in data_sets for d in data),
]
distance = value_range[1] - value_range[0]

graph_rows = []
for data in data_sets:
    step = distance / levels
    horizon_bars = []
    for d in data:
        level = int((d - value_range[0]) // step)
        horizon_bars.append(
            Bar(
                (d - value_range[0]) % step,
                (0, step),
                length=9,
                orientation="vertical",
                color=colors[level],
                bgcolor=colors[level - 1] if level > 0 else None,
            )
        )
    graph_rows.append(Horizontal(*horizon_bars))
graph = Vertical(*graph_rows, gap=1)

console = Console()
console.print(graph)
