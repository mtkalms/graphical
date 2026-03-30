from data import data_density as data
from graphical.data._pairs import pairs
from graphical.group import Horizontal, Vertical
from graphical.heat import Heat
from rich.console import Console

from graphical.scale.chromatic.sequential import VIRIDIS

value_range = (min(min(d) for d in data), max(max(d) for d in data))

graph = Vertical()
for pair in pairs(data):
    line = Horizontal()
    for entries in zip(*pair):
        line.append(
            Heat(
                data=entries,
                value_range=value_range,
                scheme=VIRIDIS,
                orientation="vertical",
            )
        )
    graph.append(line)

console = Console()
console.print(graph)
