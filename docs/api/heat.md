---
title: "graphical.heat"
---

```{.rich}
import math
from graphical.group import Horizontal, Vertical
from graphical.heat import Heat

from graphical.scale.chromatic.sequential import VIRIDIS

data = [
    [
        round(
            0.5
            + 0.28 * math.sin(r / 1.7)
            + 0.22 * math.cos(c * 0.9 + r / 4)
            + 0.14 * math.sin((r + 1) * (c + 1) / 5)
            + 0.08 * math.cos((c - r) * 1.6),
            3,
        ) for c in range(12)
    ] for r in range(10)
]

value_range = (min(min(d) for d in data), max(max(d) for d in data))

lines = []
for line in data:
    cells = []
    for entry in line:
        cells.append(
            Heat(
                data=entry,
                value_range=value_range,
                scheme=VIRIDIS,
                repeat_x=4,
                repeat_y=2,
            )
        )
    lines.append(Horizontal(*cells))
heatmap = Vertical(*lines)


data = [
    [
        round(
            0.08
            + 0.9 * math.exp(-(((c - 25) / 18) ** 2 + ((r - 18) / 7.2) ** 2))
            + 0.2
            * math.cos(
                0.6 * math.sqrt(((c - 25) / 1) ** 2 + ((r - 18) / 1.65) ** 2)
            )
            * math.exp(-(((c - 25) / 28) ** 2 + ((r - 18) / 12.6) ** 2)),
            3,
        )
        for c in range(50)
    ]
    for r in range(40)
]

value_range = (min(min(d) for d in data), max(max(d) for d in data))

lines = []
for pair in zip(data[::2], data[1::2]):
    cells = []
    for entries in zip(*pair):
        cells.append(
            Heat(
                data=entries,
                value_range=value_range,
                scheme=VIRIDIS,
                orientation="vertical",
            )
        )
    lines.append(Horizontal(*cells))
densityplot = Vertical(*lines)
output = Horizontal(heatmap, densityplot, gap=2)
```

```glyphs
single: [green]█[/]    horizontal: [green on blue]▌[/]    vertical: [green on blue]▄[/]
```

::: graphical.heat