from rich.console import Console

from graphical.bar import Stack
from graphical.group import Horizontal
from data import data_stacked as data

max_sum = max(sum(d) for d in data)

stacks = []
for d in data:
    stacks.append(Stack(d, (0, max_sum), orientation="vertical"))
graph = Horizontal(*stacks)

console = Console()
console.print(graph)
