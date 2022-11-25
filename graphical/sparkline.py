from enum import Enum
from typing import Union, List

from rich.color import Color
from rich.console import ConsoleOptions, RenderResult, Console
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style


class SparklineStyle(Enum):
    AREA = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
    LINE = ['▁', '⎽', '⎼', '─', '⎻', '⎺', '▔', '▔']

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, chars: List[str]):
        self.chars = chars


class Sparkline:

    def __init__(
        self,
        values: List[float],
        color: Union[Color, str] = "default",
        bgcolor: Union[Color, str] = "default",
        graph_style: SparklineStyle = SparklineStyle.AREA
    ):
        self.style = Style(color=color, bgcolor=bgcolor)
        self.values = values
        self.chars = graph_style.chars

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        lower, upper = min(self.values), max(self.values)
        steps = (upper - lower) / (len(self.chars) - 1)
        graph = ""
        for value in self.values:
            idx = int((value - lower) // steps)
            graph += self.chars[idx]
        yield Segment(graph, self.style)
        yield Segment("\n")

    def __rich_measure__(self, console: Console, options: ConsoleOptions) -> Measurement:
        width = len(self.values)
        return Measurement(width, width)


if __name__ == '__main__':
    from rich import print
    from random import randint
    from math import sin, pi

    for style in SparklineStyle:
        print(style.name)
        print()

        data = [randint(0, 100) for d in range(100)]
        line = Sparkline(data, color="blue", graph_style=style)
        print(line)
        print()

        data = [sin(2 * pi * d / 10) for d in range(100)]
        line = Sparkline(data, color="purple", graph_style=style)
        print(line)
        print()
