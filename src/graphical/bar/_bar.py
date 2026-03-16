from typing import Generator, Literal, Tuple, Optional, Union

from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.segment import Segment
from rich.measure import Measurement
from rich.style import Style

from ._cell_value import _cell_value
from graphical.utils import invert_style, InversionStrategy
from graphical.mark import Mark
from graphical.mark.horizontal import BAR_BLOCK_H
from graphical.mark.vertical import BAR_BLOCK_V
from graphical.section import Section

Numeric = Union[int, float]
Orientation = Literal["horizontal", "vertical"]


class Bar:
    """Bar graph.

    Args:
        data (Numeric): The value.
        value_range: Lower and upper boundary.
        length (int): The length of the graph. Defaults to 100.
        marks (Union[BarMark, Mark]], optional): Marks used for the bar. Defaults to "block".
        color (Union[Color, str], optional): Color of the bar. Defaults to "default".
        bgcolor (Union[Color, str], optional): Background color. Defaults to "default".
        invert_negative (Literal["reverse",  "swap"], optional): Use positive marks and invert cell colors for negative number. If None or not supported by marks, the cell is not inverted.
        orientation: (Literal["horizontal", "vertical"], optional): The orientation of the bar. Defaults to "horizontal".
        origin (Numeric, optional): Origin point. Defaults to 0.0.
        force_origin (bool, optional): Force origin to half cell grid. Defaults to False.
    """

    def __init__(
        self,
        value: Numeric,
        value_range: Tuple[Numeric, Numeric],
        *,
        length: Optional[int] = None,
        marks: Optional[Mark] = None,
        color: Optional[Union[Color, str]] = None,
        bgcolor: Optional[Union[Color, str]] = None,
        invert_negative: Optional[InversionStrategy] = None,
        orientation: Orientation = "horizontal",
        origin: Optional[Numeric] = None,
        force_origin: Optional[bool] = None,
    ) -> None:
        self.value = value
        self.value_range = value_range
        self.length = length or 100
        self.marks = marks or (
            BAR_BLOCK_H if orientation == "horizontal" else BAR_BLOCK_V
        )
        self.color = color
        self.bgcolor = bgcolor
        self.invert_negative: Optional[InversionStrategy] = invert_negative
        self.orientation = orientation
        self.origin = origin or 0.0
        self.force_origin = force_origin is not False

    def _invertible(self) -> bool:
        if not self.marks.invertible or self.invert_negative is None:
            return False
        if self.invert_negative == "swap":
            return all(d not in [None, "default"] for d in [self.color, self.bgcolor])
        elif self.invert_negative == "reverse":
            return True
        else:
            return False

    def segments(self, length: Optional[int] = None) -> Generator[Segment]:
        """Returns rendered bar segments.

        Args:
            length (Optional[int], optional): Override bar graph length.
        Yields:
            _type_:Rendered bar segments.
        """
        length = length or self.length
        vertical = self.orientation == "vertical"
        style = Style(color=self.color, bgcolor=self.bgcolor)
        bar = Section(min(self.origin, self.value), max(self.origin, self.value))

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
            cell_value = _cell_value(bar, segment, force_origin=self.force_origin)
            invert = cell_value < 0 and self._invertible()
            invert_mark = invert and self.invert_negative == "swap"
            cell_style = invert_style(style, self.invert_negative) if invert else style
            if self.value in segment and self.value != segment.lower:
                # Use cap character for the upper boundary of the bar
                cell_char = self.marks.cap(cell_value, invert_mark)
            else:
                cell_char = self.marks.get(cell_value, invert_mark)
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
