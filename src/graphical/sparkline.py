from collections.abc import Generator
from typing import Callable, Sequence, TypeVar, Tuple

from click import Tuple
from rich.color import Color
from rich.console import ConsoleOptions, RenderResult, Console
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from graphical._buckets import buckets, SummaryFunction
from graphical._normalize import normalize
from graphical.mark import *

Numeric = TypeVar("T", int, float)


class Sparkline:
    def __init__(
        self,
        values: Sequence[Numeric],
        value_range: Tuple[Numeric, Numeric],
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

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        style = Style(color=self.color, bgcolor=self.bgcolor)
        for cell_value in buckets(self.values, self.width, self.summary_function):
            normalized = normalize(cell_value, self.value_range)
            cell_char = self.cells.get(normalized)
            yield Segment(cell_char, style=style)

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, 1)
