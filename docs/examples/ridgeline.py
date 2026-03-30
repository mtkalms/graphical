from rich.console import Console

from graphical.bar import Bar
from graphical.group import Horizontal
from graphical.layer import Layers
from graphical.offset import Offset
from graphical.scale.chromatic.sequential import VIRIDIS
from data import data_ridgeline as data


value_range = (0, max(max(d) for d in data))

colors = VIRIDIS.palette(10)
graph = Layers()
for idx, line_data in enumerate(data):
    line = Horizontal()
    for value in line_data:
        line.append(
            Bar(
                value,
                value_range,
                length=5,
                color=colors[idx],
                orientation="vertical",
            )
        )
    graph.append(Offset(line, 0, idx * 2))

console = Console()
console.print(graph)
