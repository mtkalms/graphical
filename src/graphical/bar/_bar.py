from typing import Iterable, Tuple, Optional, Union

from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.segment import Segment, Segments
from rich.measure import Measurement
from rich.style import Style

from graphical.mark import Mark
from graphical.mark.horizontal import BAR_BLOCK_H
from graphical.mark.vertical import BAR_BLOCK_V
from graphical.section import Section

from ._invert_style import invert_style, InversionStrategy
from ._overlap import overlap
from ._types import Orientation, Numeric


class Bar:
    """Bar graph.

    Args:
        data (Numeric): The value.
        value_range: Lower and upper boundary.
        length (int): The length of the graph. Defaults to 100.
        width (int): The width of the bars. Defaults to 1.
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
        data: Numeric,
        value_range: Tuple[Numeric, Numeric],
        *,
        length: Optional[int] = None,
        width: Optional[int] = None,
        marks: Optional[Mark] = None,
        color: Optional[Union[Color, str]] = None,
        bgcolor: Optional[Union[Color, str]] = None,
        invert_negative: Optional[InversionStrategy] = None,
        orientation: Orientation = "horizontal",
        origin: Optional[Numeric] = None,
        force_origin: Optional[bool] = None,
    ) -> None:
        self.value = data
        self.value_range = value_range
        self.length = length or 100
        self.width = width or 1
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

    def segments(self, length: Optional[int] = None) -> Iterable[Segment]:
        """Returns rendered bar segments.

        Args:
            length (Optional[int], optional): Override bar graph length.
        Yields:
            Segment: Next segment of rendered bar.
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
            cell_value = overlap(bar, segment, force_origin=self.force_origin)
            invert = cell_value < 0 and self._invertible()
            invert_mark = invert and self.invert_negative is not None
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

    def __graphical_group__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        if self.orientation in "horizontal":
            length = min(self.length, options.max_width)
            yield Segments(Segment.simplify(self.segments(length)))
            if self.width > 1:
                yield Segments(
                    [Segment.line(), *Segment.simplify(self.segments(length))]
                    * (self.width - 1)
                )
        else:
            length = min(self.length, options.max_height)
            for segment in self.segments(length):
                yield Segments([segment] * self.width)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        line_segments = self.__graphical_group__(console, options)
        if self.orientation in "horizontal":
            yield from line_segments
        else:
            for segment in line_segments:
                yield segment
                yield Segment.line()

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(5, options.max_width)
