from rich.console import Console
from graphical.bar import Stack
from graphical.group import Horizontal
from data import data_stacked as data

max_sum = max(sum(d) for d in data)

graph = Horizontal(gap=1)
for d in data[:34]:
    graph.append(
        Stack(
            d,
            (0, max_sum),
            orientation="vertical",
            width=2,
            length=15,
        )
    )

console = Console()
console.print(graph)
