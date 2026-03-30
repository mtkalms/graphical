from rich.console import Console

from graphical.bar import Stack
from graphical.group import Horizontal
from data import data_stacked as data

max_sum = max(sum(d) for d in data)

graph = Horizontal()
for d in data:
    graph.append(
        Stack(
            d,
            (0, max_sum),
            orientation="vertical",
        )
    )

console = Console()
console.print(graph)
