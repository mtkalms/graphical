from data import data_density as data
from graphical.heat import Heat
from rich.console import Console

from graphical.scale.chromatic.sequential import VIRIDIS

value_range = (min(min(d) for d in data), max(max(d) for d in data))

console = Console()
for pair in zip(data[1::2], data[::2]):
    for entries in zip(*pair):
        console.print(
            Heat(
                data=entries,
                value_range=value_range,
                scheme=VIRIDIS,
                orientation="vertical",
            )
        )
    console.print()
