from rich.console import Console
from graphical.group import Horizontal, Vertical
from graphical.heat import Heat
from graphical.scale.chromatic.sequential import VIRIDIS
from data import data_heatmap as data

value_range = (
    min(min(d) for d in data),
    max(max(d) for d in data),
)

graph = Vertical()
for data_line in data:
    line = Horizontal()
    for entry in data_line:
        line.append(
            Heat(
                data=entry,
                value_range=value_range,
                scheme=VIRIDIS,
                repeat_x=4,
                repeat_y=2,
            )
        )
    graph.append(line)

console = Console()
console.print(graph)
