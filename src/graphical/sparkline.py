from collections.abc import Generator
from typing import Callable, Sequence, TypeVar, Tuple

from click import Tuple
from rich.color import Color
from rich.console import ConsoleOptions, RenderResult, Console
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from graphical.mark import *

T = TypeVar("T", int, float)

SummaryFunction = Callable[[Sequence[T]], float]


class Sparkline:
    def __init__(
        self,
        values: Sequence[T],
        value_range: Tuple[T, T],
        width: int = None,
        cells: Mark = BAR_BLOCK_V,
        color: Color = None,
        bgcolor: Color = None,
        summary_function: SummaryFunction = max,
    ):
        self.values = values
        self.value_range = value_range
        self.width = width or len(values)
        self.cells = cells
        self.color = color
        self.bgcolor = bgcolor
        self.summary_function = summary_function

    @classmethod
    def segments(
        cls, values: Sequence[T], count: int, summary_function: SummaryFunction
    ) -> Generator[float]:
        step = len(values) / count
        for d in range(count):
            segment = values[int(d * step) : int((d + 1) * step)]
            yield summary_function(segment)

    @classmethod
    def normalize(cls, value: T, value_range: Tuple[T, T]) -> float:
        result = (value - value_range[0]) / (value_range[1] - value_range[0])
        return min(max(result, 0.0), 1.0)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        style = Style(color=self.color, bgcolor=self.bgcolor)
        for cell_value in self.segments(self.values, self.width, self.summary_function):
            normalized = self.normalize(cell_value, self.value_range)
            cell_char = self.cells.get(normalized)
            yield Segment(cell_char, style=style)

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, 1)


if __name__ == "__main__":
    from rich.console import Console

    console = Console()

    for markers in [
        BAR_BLOCK_V,
        BAR_HEAVY_V,
        BAR_LIGHT_V,
        BAR_SHADE,
    ]:
        console.print(
            Sparkline(
                values=[row_value for row_value in range(-50, 50)],
                value_range=(-50, 50),
                width=100,
                cells=markers,
            )
        )
        print()
        print()
