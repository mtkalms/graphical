from rich.console import Console

from graphical.bar import RangeStack
from graphical.group import Vertical
from data import data_gantt as data


lanes = []
for start, stop, progress in data:
    length = stop - start
    lanes.append(
        RangeStack(
            (start, length * progress, length * (1.0 - progress)),
            (0, 1),
            orientation="horizontal",
            colors=["purple", "red"],
        )
    )

graph = Vertical(*lanes, gap=1)

console = Console()
console.print(graph)
