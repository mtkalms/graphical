from typing import Literal, Tuple, Optional, Union

from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.segment import Segment
from rich.measure import Measurement
from rich.style import Style

from ._cell_value import _cell_value
from graphical.utils import invert_style
from graphical.mark import Mark, BAR_BLOCK_H, BAR_BLOCK_V
from graphical.section import Section

Numeric = Union[int, float]
Orientation = Literal["horizontal", "vertical"]


class Bar:
    def __init__(
        self,
        value: Numeric,
        value_range: Tuple[Numeric, Numeric],
        *,
        length: Optional[int] = None,
        marks: Optional[Mark] = None,
        color: Optional[Union[Color, str]] = None,
        bgcolor: Optional[Union[Color, str]] = None,
        invert_negative: bool = False,
        orientation: Orientation = "horizontal",
    ) -> None:
        self.value = value
        self.value_range = value_range
        self.length = length or 100
        self.marks = marks or (
            BAR_BLOCK_H if orientation == "horizontal" else BAR_BLOCK_V
        )
        self.color = color
        self.bgcolor = bgcolor
        self.invert_negative = invert_negative
        self.orientation = orientation

    def _invertible(self) -> bool:
        return (
            self.invert_negative
            and self.color not in [None, "default"]
            and self.bgcolor not in [None, "default"]
            and self.marks.invertible
        )

    def segments(self, length: Optional[int] = None):
        length = length or self.length
        vertical = self.orientation == "vertical"
        style = Style(color=self.color, bgcolor=self.bgcolor)
        bar = Section(min(0, self.value), max(0, self.value))

        lower, upper = self.value_range
        step = abs(upper - lower) / length
        inset = max(int((bar.lower - lower) // step), 0)
        trail = max(int((upper - bar.upper) // step), 0)
        length = length - (inset + trail)

        # Handle Whitespace
        base_style = Style(bgcolor=self.bgcolor)
        for _ in range(trail if vertical else inset):
            yield Segment(" ", style=base_style)

        segments = Section(lower + inset * step, upper - trail * step).segment(length)
        if vertical:
            segments = list(segments)[::-1]
        for segment in segments:
            cell_value = _cell_value(bar, segment)
            invert = cell_value < 0 and self._invertible()
            cell_style = invert_style(style) if invert else style
            if self.value in segment and self.value != segment.lower:
                # Use cap character for the upper boundary of the bar
                cell_char = self.marks.cap(cell_value, invert)
            else:
                cell_char = self.marks.get(cell_value, invert)
            yield Segment(cell_char, style=cell_style)

        # Handle whitespace
        for _ in range(inset if vertical else trail):
            yield Segment(" ", style=base_style)

    def __iter__(self):
        return self.segments()

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        if self.orientation in "horizontal":
            width = min(self.length, options.max_width)
            yield from Segment.simplify(self.segments(width))
        else:
            height = min(self.length, options.max_height)
            for segment in self.segments(height):
                yield segment
                yield Segment.line()

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(5, options.max_width)
