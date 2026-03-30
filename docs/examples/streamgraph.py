from rich.console import Console

from graphical.bar import Stack
from graphical.group import Horizontal
from data import data_stacked as data

max_sum = max(sum(d) for d in data)

stacks = []
for d in data:
    offset = (max_sum - sum(d)) / 2.0
    stacks.append(
        Stack(
            d,
            (-offset, -offset + max_sum),
            orientation="vertical",
        )
    )
graph = Horizontal(*stacks)

console = Console()
console.print(graph)
