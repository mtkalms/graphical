from typing import Iterable, Sequence, Tuple, Optional, Union

from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.segment import Segment
from rich.measure import Measurement
from rich.style import Style

from graphical.mark import Mark
from graphical.mark.horizontal import BAR_BLOCK_H
from graphical.mark.vertical import BAR_BLOCK_V
from graphical.section import Section

from ._invert_style import invert_style, InversionStrategy
from ._overlap import overlap
from ._types import Orientation, Numeric


class Stack:
    """Stacked bar graph.

    Args:
        values (Sequence[Numeric]): The values in order of stacking.
        value_range: Lower and upper boundary. Defaults to range of data.
        width (int): The width of the graph. Defaults to 100.
        marks (Union[BarMark, Mark]], optional): Marks used for the bars. Defaults to "block".
        colors (Sequence[Union[Color, str]], optional): Colors of the bars.
        bgcolor (Union[Color, str], optional): Background color. Defaults to "default".
        invert_negative (Literal["reverse",  "swap"], optional): Use positive marks and invert cell colors for negative number. If None or not supported by marks, the cell is not inverted.
        orientation: (Literal["horizontal", "vertical"], optional): The orientation of the bar. Defaults to "horizontal".
        origin (Numeric, optional): Origin point. Defaults to 0.0.
        force_origin (bool, optional): Force origin to half cell grid. Defaults to False.
    """

    def __init__(
        self,
        values: Sequence[Numeric],
        value_range: Tuple[Numeric, Numeric],
        *,
        length: Optional[int] = None,
        marks: Optional[Mark] = None,
        colors: Sequence[Union[Color, str]] = ["red", "green", "blue", "yellow"],
        bgcolor: Optional[Union[Color, str]] = None,
        invert_negative: Optional[InversionStrategy] = None,
        orientation: Orientation = "horizontal",
        origin: Optional[Numeric] = None,
        force_origin: Optional[bool] = None,
    ) -> None:
        self.values = values
        self.value_range = value_range
        self.length = length or 100
        self.marks = marks or (
            BAR_BLOCK_H if orientation == "horizontal" else BAR_BLOCK_V
        )
        self.colors = colors
        self.bgcolor = bgcolor
        self.orientation = orientation
        self.invert_negative: Optional[InversionStrategy] = invert_negative
        self.origin = origin or 0.0
        self.force_origin = force_origin is not False

    def _stacked_colors(self) -> Sequence[Color]:
        colors = []
        for idx, value in enumerate(self.values):
            if value >= self.origin:
                colors.append(self.colors[idx % len(self.colors)])
            else:
                colors.insert(0, self.colors[idx % len(self.colors)])
        return colors

    def _stacked_values(self) -> Sequence[Numeric]:
        pos = []
        neg = []
        for value in self.values:
            stack = pos if value >= self.origin else neg
            cumulative = stack[-1] if stack else self.origin
            stack.append(cumulative + value)
        return neg[::-1] + [self.origin] + pos

    def _stacked_bars(self, values: Sequence[Numeric]) -> Sequence[Section]:
        return [Section(*bounds) for bounds in zip(values[:-1], values[1:])]

    def _invertible(self, color: Union[Color, str]) -> bool:
        if not self.marks.invertible or self.invert_negative is None:
            return False
        if self.invert_negative == "swap":
            return all(d not in [None, "default"] for d in [color, self.bgcolor])
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

        colors = self._stacked_colors()
        bounds = self._stacked_values()
        bars = self._stacked_bars(bounds)

        lower, upper = self.value_range
        bar_lower = bounds[0]
        bar_upper = bounds[-1]
        step = abs(upper - lower) / length
        inset = max(int((bar_lower - lower) // step), 0)
        trail = max(int((upper - bar_upper) // step), 0)
        length = length - (inset + trail)

        # Handle Whitespace
        base_style = Style(bgcolor=self.bgcolor)
        for _ in range(trail if vertical else inset):
            yield Segment(" ", style=base_style)

        # Handle Segments that overlap with bars
        segments = Section(lower + inset * step, upper - trail * step).segment(length)
        if vertical:
            segments = list(segments)[::-1]
        for segment in segments:
            cell_ids = [idx for idx, bar in enumerate(bars) if bar.overlaps(segment)]
            cell_values = [
                overlap(
                    bars[idx],
                    segment,
                    origin=self.origin,
                    force_origin=self.force_origin,
                )
                for idx in cell_ids
            ]
            # No bar in segment
            if not cell_ids:
                yield Segment(" ", style=base_style)
            # One bar in segment
            elif len(cell_ids) == 1:
                cell_value = cell_values[0]
                cell_color = colors[cell_ids[0]]
                cell_style = Style(color=cell_color, bgcolor=self.bgcolor)
                invert = cell_value < 0 and self._invertible(cell_color)
                invert_mark = invert and self.invert_negative == "swap"
                if invert:
                    cell_style = invert_style(cell_style, self.invert_negative)
                yield Segment(
                    self.marks.get(cell_value, invert_mark),
                    style=cell_style,
                )
            # Multiple bars in segment
            else:
                id_values = list(zip(cell_ids, cell_values))
                trailing_id, trailing_val = max(id_values, key=lambda x: x[1])
                trailing_color = colors[trailing_id]
                leading_id, leading_val = min(id_values, key=lambda x: x[1])
                leading_color = colors[leading_id]
                if self.marks.invertible:
                    # Always use the trailing bar fragment for better resolution
                    yield Segment(
                        self.marks.get(trailing_val),
                        style=Style(color=trailing_color, bgcolor=leading_color),
                    )
                else:
                    # Use bar with more overlap to fill whole segment
                    if abs(trailing_val) > abs(leading_val):
                        cell_char = self.marks.get(1.0)
                        color = trailing_color
                    else:
                        cell_char = self.marks.get(-1.0)
                        color = leading_color
                    yield Segment(
                        cell_char,
                        style=Style(color=color, bgcolor=self.bgcolor),
                    )

        # Handle whitespace
        for _ in range(inset if vertical else trail):
            yield Segment(" ", style=base_style)

    def __vertical__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        height = min(self.length, options.max_height)
        for segment in self.segments(height):
            yield segment

    def __horizontal__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        width = min(self.length, options.max_width)
        yield from Segment.simplify(self.segments(width))

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        if self.orientation in "horizontal":
            yield from self.__horizontal__(console, options)
        else:
            for segment in self.__vertical__(console, options):
                yield segment
                yield Segment.line()

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(5, options.max_width)
