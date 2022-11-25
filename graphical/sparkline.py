from enum import Enum
from typing import Union, List, Optional, Tuple

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
        self.chars: List[str] = chars
        self.last: int = len(self.chars) - 1


class SparklineRenderer:

    @staticmethod
    def render(
        values: List[float],
        value_range: Optional[Tuple[float, float]] = None,
        graph_style: SparklineStyle = SparklineStyle.AREA
    ) -> str:
        if value_range:
            lower, upper = value_range
        else:
            lower, upper = min(values), max(values)
        steps = (upper - lower) / graph_style.last
        graph = ""
        for value in values:
            if value > upper:
                idx = graph_style.last
            elif value < lower:
                idx = 0
            else:
                idx = int((value - lower) / steps)
            graph += graph_style.chars[idx]
        return graph


class Sparkline:

    def __init__(
        self,
        values: List[float],
        value_range: Optional[Tuple[float, float]] = None,
        color: Union[Color, str] = "default",
        bgcolor: Union[Color, str] = "default",
        graph_style: SparklineStyle = SparklineStyle.AREA
    ):
        self.values = values
        self.value_range = value_range
        self.style = Style(color=color, bgcolor=bgcolor)
        self.graph_style = graph_style

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        graph = SparklineRenderer.render(self.values, self.value_range, self.graph_style)
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
        line = Sparkline(data, value_range=(0, 2), color="purple", graph_style=style)
        print(line)
        print()
