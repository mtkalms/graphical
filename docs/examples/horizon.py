from rich.console import Console
from graphical.bar import Bar
from graphical.data import bands
from graphical.group import Horizontal, Vertical
from graphical.scale.chromatic.sequential import GREENS
from data import data_horizon as data_sets

levels = 4
colors = GREENS.palette(levels)
value_range = (
    min(d for data in data_sets for d in data),
    max(d for data in data_sets for d in data),
)

graph = Vertical(gap=1)
for data in data_sets:
    horizon = Horizontal()
    for level, value in bands(data, levels):
        horizon.append(
            Bar(
                value if level < levels else 0.0,
                (0, 1),
                length=9,
                orientation="vertical",
                color=colors[level] if level < levels else None,
                bgcolor=colors[level - 1] if level > 0 else None,
            )
        )
    graph.append(horizon)

console = Console()
console.print(graph)
