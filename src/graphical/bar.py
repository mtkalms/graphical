from typing import Literal, Sequence, Tuple, Optional, TypeVar

from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.segment import Segment, Segments
from rich.measure import Measurement
from rich.style import Style


from graphical._invert_style import invert_style
from graphical.mark import Mark, BAR_BLOCK_H, BAR_BLOCK_V
from graphical.section import Section

Numeric = TypeVar("T", int, float)
Orientation = Literal["horizontal", "vertical"]


def _cell_value(bar: Section, segment: Section) -> float:
    intersection = segment.intersect(bar)
    # No intersection
    if not intersection:
        cell_value = 0.0
    # Full intersection
    elif segment == intersection:
        sign = -1.0 if bar.lower < 0 else 1.0
        cell_value = sign * 1.0
    # Partial intersection
    else:
        sign = 1.0 if intersection.middle < segment.middle else -1.0
        # Handle origin that falls between segment boundaries
        if segment.lower < 0.0 < segment.upper:
            cell_value = sign * -0.0 if bar in segment else sign * 0.5
        else:
            cell_value = sign * intersection.length / segment.length
    return cell_value


class Bar:
    def __init__(
        self,
        value: Numeric,
        value_range: Tuple[Numeric, Numeric],
        width: int,
        marks: Optional[Mark] = None,
        color: Optional[Color] = None,
        bgcolor: Optional[Color] = None,
        invert_negative: bool = False,
        orientation: Orientation = "horizontal",
    ) -> None:
        self.value = value
        self.value_range = value_range
        self.width = width
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

    def __iter__(self):
        style = Style(color=self.color, bgcolor=self.bgcolor)
        bar = Section(min(0, self.value), max(0, self.value))
        segments = Section(*self.value_range).segment(self.width)
        if self.orientation == "vertical":
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

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        for segment in self:
            yield segment
            if self.orientation in "vertical":
                yield Segment.line()

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, 1)


class StackedBar:
    def __init__(
        self,
        values: Sequence[Numeric],
        value_range: Tuple[Numeric, Numeric],
        width: int,
        marks: Optional[Mark] = None,
        colors: Sequence[Color] = ["red", "green", "blue", "yellow"],
        bgcolor: Optional[Color] = None,
        invert_negative: bool = True,
        orientation: Orientation = "horizontal",
    ) -> None:
        self.values = values
        self.value_range = value_range
        self.width = width
        self.marks = marks or (
            BAR_BLOCK_H if orientation == "horizontal" else BAR_BLOCK_V
        )
        self.colors = colors
        self.bgcolor = bgcolor
        self.orientation = orientation
        self.invert_negative = invert_negative

    def _stacked_colors(self) -> Sequence[Color]:
        colors = []
        for idx, value in enumerate(self.values):
            if value >= 0:
                colors.append(self.colors[idx % len(self.colors)])
            else:
                colors.insert(0, self.colors[idx % len(self.colors)])
        return colors

    def _stacked_values(self) -> Sequence[Numeric]:
        pos = []
        neg = []
        for value in self.values:
            stack = pos if value >= 0 else neg
            cummulative = stack[-1] if stack else 0.0
            stack.append(cummulative + value)
        return neg[::-1] + [0.0] + pos

    def _stacked_bars(self, values: Sequence[Numeric]) -> Sequence[Section]:
        return [Section(*bounds) for bounds in zip(values[:-1], values[1:])]

    def _invertible(self) -> bool:
        return (
            self.invert_negative
            and self.bgcolor not in [None, "default"]
            and self.marks.invertible
        )

    def __iter__(self):
        vertical = self.orientation == "vertical"

        colors = self._stacked_colors()
        bounds = self._stacked_values()
        bars = self._stacked_bars(bounds)

        lower, upper = self.value_range
        bar_lower = bounds[0]
        bar_upper = bounds[-1]
        step = abs(upper - lower) / self.width
        inset = max(int((bar_lower - lower) // step), 0)
        trail = max(int((upper - bar_upper) // step), 0)
        width = self.width - (inset + trail)

        # Handle Whitespace
        base_style = Style(bgcolor=self.bgcolor)
        for _ in range(trail if vertical else inset):
            yield Segment(" ", style=base_style)

        # Handle Segments that overlap with bars
        segments = Section(lower + inset * step, upper - trail * step).segment(width)
        if self.orientation == "vertical":
            segments = list(segments)[::-1]
        for segment in segments:
            cell_ids = [idx for idx, bar in enumerate(bars) if bar.overlaps(segment)]
            cell_values = [_cell_value(bars[idx], segment) for idx in cell_ids]
            # No bar in segment
            if not cell_ids:
                yield Segment(" ", style=base_style)
            # One bar in segment
            elif len(cell_ids) == 1:
                cell_value = cell_values[0]
                invert = cell_value < 0 and self._invertible()
                if invert:
                    cell_style = Style(color=self.bgcolor, bgcolor=colors[cell_ids[0]])
                else:
                    cell_style = Style(color=colors[cell_ids[0]], bgcolor=self.bgcolor)
                yield Segment(
                    self.marks.get(cell_value, invert),
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

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        for segment in self:
            yield segment
            if self.orientation in "vertical":
                yield Segment.line()

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, 1)


def main():
    from rich.console import Console
    from graphical.mark import (
        BAR_HEAVY_H,
        BAR_LIGHT_H,
        BAR_BLOCK_V,
        BAR_HEAVY_V,
        BAR_LIGHT_V,
    )

    console = Console()

    width = 15

    bars = []
    for markers in [
        BAR_BLOCK_V,
        BAR_HEAVY_V,
        BAR_LIGHT_V,
    ]:
        for row_value in range(-20, 21):
            bars.append(
                Bar(
                    value=row_value / 4.3,
                    value_range=(-5.1, 5.1),
                    width=width,
                    marks=markers,
                    color="red",
                    bgcolor="black",
                    invert_negative=True,
                    orientation="vertical",
                )
            )
    for d in range(width):
        console.print(Segments([list(bar)[d] for bar in bars]))
        console.print()

    width = 60
    bars = []
    for markers in [
        (BAR_BLOCK_V, BAR_BLOCK_H),
        (BAR_HEAVY_V, BAR_HEAVY_H),
        (BAR_LIGHT_V, BAR_LIGHT_H),
    ]:
        for idx, values in enumerate(
            [
                [20, 25, 30, 1, 35],
                [15, 20, 10, 25],
                [10, 15, 12, 18],
                [12, 10, 15, 11],
                [-20, -25, -30, -35],
                [-15, -20, -10, -25],
                [-10, -15, -12, -18],
                [-12, -10, -15, -11],
                [20, -25, 30, -35],
                [15, -20, 10, 25],
                [10, 15, -12, 18],
                [12, 10, 15, -11],
                [20, 25, 30, 1, 35],
                [20, 25, 30, 1, 34],
                [20, 25, 30, 1, 33],
                [20, 25, 30, 1, 32],
                [20, 25, 30, 1, 31],
                [20, 25, 30, 1, 30],
                [20, 25, 30, 1, 29],
                [20, 25, 30, 1, 28],
                [20, 25, 30, 1, 27],
                [20, 25, 30, 1, 26],
                [-20, -25, -30, -1, -35],
                [-20, -25, -30, -1, -34],
                [-20, -25, -30, -1, -33],
                [-20, -25, -30, -1, -32],
                [-20, -25, -30, -1, -31],
                [-20, -25, -30, -1, -29],
                [-20, -25, -30, -1, -28],
                [-20, -25, -30, -1, -27],
                [-20, -25, -30, -1, -26],
            ]
        ):
            console.print(
                StackedBar(
                    values=values,
                    value_range=(-120, 120),
                    width=width,
                    marks=markers[1],
                    colors=["green", "blue", "purple", "magenta", "yellow"],
                    bgcolor="black",
                )
            )
            console.print()
            bars.append(
                list(
                    StackedBar(
                        values=values,
                        value_range=(-120, 120),
                        width=width,
                        marks=markers[0],
                        colors=["green", "blue", "purple", "magenta", "yellow"],
                        bgcolor="black",
                        orientation="vertical",
                    )
                )
            )

    for d in range(width):
        console.print(Segments([bar[d] for bar in bars]))
        console.print()


if __name__ == "__main__":
    main()
