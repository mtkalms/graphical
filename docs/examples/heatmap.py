from data import data_heatmap as data
from graphical.group import Horizontal
from graphical.heat import Heat
from rich.console import Console

from graphical.scale.chromatic.sequential import VIRIDIS

value_range = (min(min(d) for d in data), max(max(d) for d in data))

console = Console()
for line in data:
    cells = []
    for entry in line:
        cells.append(
            Heat(
                data=entry,
                value_range=value_range,
                scheme=VIRIDIS,
                repeat_x=6,
                repeat_y=3,
            )
        )
    console.print(Horizontal(*cells))
    console.print()
