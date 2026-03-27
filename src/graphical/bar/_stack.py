from typing import Iterable, Sequence, Tuple, Optional, Union

from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.segment import Segment, Segments
from rich.measure import Measurement
from rich.style import Style

from graphical.mark import Mark
from graphical.mark.horizontal import BAR_BLOCK_H
from graphical.mark.vertical import BAR_BLOCK_V
from graphical.section import Section
from graphical.scale.chromatic.ordinal import CATEGORY10

from ._invert_style import invert_style, InversionStrategy
from ._overlap import overlap
from ._types import OptimizationStrategy, Orientation, Numeric


class Stack:
    """Stacked bar graph.

    Args:
        data (Sequence[Numeric]): The values in order of stacking.
        value_range: Lower and upper boundary. Defaults to range of data.
        length (int): The length of the graph. Defaults to 100.
        width (int): The width of the bars. Defaults to 1.
        marks (Union[BarMark, Mark]], optional): Marks used for the bars. Defaults to "block".
        colors (Sequence[Union[Color, str]], optional): Colors of the bars.
        bgcolor (Union[Color, str], optional): Background color. Defaults to "default".
        invert_negative (Literal["reverse",  "swap"], optional): Use positive marks and invert cell colors for negative number. If None or not supported by marks, the cell is not inverted.
        orientation: (Literal["horizontal", "vertical"], optional): The orientation of the bar. Defaults to "horizontal".
        origin (Numeric, optional): Origin point. Defaults to 0.0.
        force_origin (bool, optional): Force origin to half cell grid. Defaults to False.
        prefer_bg (OptimizationStrategy): Replace block characters with background, either "never", for "full" blocks only, or for all. Defaults to "full".
    """

    def __init__(
        self,
        data: Sequence[Numeric],
        value_range: Tuple[Numeric, Numeric],
        *,
        length: Optional[int] = None,
        width: Optional[int] = None,
        marks: Optional[Mark] = None,
        colors: Sequence[Union[Color, str]] = CATEGORY10.colors,
        bgcolor: Optional[Union[Color, str]] = None,
        invert_negative: Optional[InversionStrategy] = None,
        orientation: Orientation = "horizontal",
        origin: Optional[Numeric] = None,
        force_origin: Optional[bool] = None,
        prefer_bg: Optional[OptimizationStrategy] = None,
    ) -> None:
        self.values = data
        self.value_range = value_range
        self.length = length or 25
        self.width = width or 1
        self.marks = marks or (
            BAR_BLOCK_H if orientation == "horizontal" else BAR_BLOCK_V
        )
        self.colors = colors
        self.bgcolor = bgcolor
        self.orientation = orientation
        self.invert_negative: Optional[InversionStrategy] = invert_negative
        self.origin = origin or 0.0
        self.force_origin = force_origin is not False
        self.prefer_bg = prefer_bg or "full"

    def _stacked_colors(self) -> Sequence[Color]:
        colors = []
        for idx, value in enumerate(self.values):
            if value >= 0.0:
                colors.append(self.colors[idx % len(self.colors)])
            else:
                colors.insert(0, self.colors[idx % len(self.colors)])
        return colors

    def _stacked_values(self) -> Sequence[Numeric]:
        pos = []
        neg = []
        for value in self.values:
            stack = pos if value >= 0.0 else neg
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

    def _optimize_bg(self, value: float, style: Style) -> Optional[Segment]:
        if self.prefer_bg == "full" and self.marks.get(value) == "█":
            # Replace full blocks with background
            return Segment(" ", style=invert_style(style))
        if self.prefer_bg == "all" and self.marks.invertible:
            # Replace all blocks with background
            style = invert_style(style) if abs(value) >= 0.5 else style
            return Segment(" ", style=style)
        return None

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
            cell_ids = []
            cell_values = []
            for idx, bar in enumerate(bars):
                if not bar.overlaps(segment):
                    continue
                cell_value = overlap(
                    bar,
                    segment,
                    origin=self.origin,
                    force_origin=self.force_origin,
                )
                if cell_value == 0.0:
                    continue
                cell_ids.append(idx)
                cell_values.append(cell_value)
            # No bar in segment
            if not cell_ids:
                yield Segment(" ", style=base_style)
            # One bar in segment
            elif len(cell_ids) == 1:
                cell_value = cell_values[0]
                cell_color = colors[cell_ids[0] % len(colors)]
                cell_style = Style(color=cell_color, bgcolor=self.bgcolor)
                # Check if background optimization can be applied
                optimized = self._optimize_bg(cell_value, cell_style)
                if optimized:
                    yield optimized
                    continue
                invert = cell_value < 0 and self._invertible(cell_color)
                invert_mark = invert and self.invert_negative is not None
                if invert:
                    cell_style = invert_style(cell_style, self.invert_negative)
                yield Segment(self.marks.get(cell_value, invert_mark), style=cell_style)
            # Multiple bars in segment
            else:
                # Use the two largest sections in order
                id_values = sorted(zip(cell_ids, cell_values), key=lambda x: x[1])
                trailing, leading = sorted(id_values[-2:], key=lambda x: x[0])
                trailing_id, trailing_val = trailing
                trailing_color = colors[trailing_id % len(colors)]
                leading_id, leading_val = leading
                leading_color = colors[leading_id % len(colors)]
                # Check if background optimization strategy can be applied
                relative_val = abs(trailing_val) / (
                    abs(leading_val) + abs(trailing_val)
                )
                default_style = Style(color=trailing_color, bgcolor=leading_color)
                optimized = self._optimize_bg(relative_val, default_style)
                if optimized:
                    # Use background instead
                    yield optimized
                elif self.marks.invertible:
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
            for segment in self.segments():
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
        if self.orientation in "horizontal":
            return Measurement(5, self.length)
        else:
            return Measurement(self.width, self.width)
