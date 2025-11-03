from typing import Literal, Sequence, Tuple, Optional, TypeVar

from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.segment import Segment, Segments
from rich.measure import Measurement
from rich.style import Style


from graphical._invert_style import invert_style
from graphical.mark import Mark, BAR_BLOCK_H
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
            if self.orientation == "vertical":
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
        invert_negative: bool = False,
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

    def _stacked_bars(self) -> Sequence[Numeric]:
        pos = []
        neg = []
        for value in self.values:
            stack = pos if value >= 0 else neg
            cummulative = stack[-1] if stack else 0.0
            stack.append(cummulative + value)
        values = neg[::-1] + [0.0] + pos
        bars = []
        for boundaries in zip(values[:-1], values[1:]):
            bars.append(Section(*boundaries))
        return bars

    def _invertible(self) -> bool:
        return (
            self.invert_negative
            and self.bgcolor not in [None, "default"]
            and self.marks.invertible
        )

    def __iter__(self):
        colors = self._stacked_colors()
        bars = self._stacked_bars()
        segments = Section(*self.value_range).segment(self.width)
        if self.orientation == "vertical":
            segments = list(segments)[::-1]
        for segment in segments:
            cell_values = [_cell_value(bar, segment) for bar in bars]
            cell_ids = [idx for idx, v in enumerate(cell_values) if v != 0.0]
            if not cell_ids:
                yield Segment(" ", style=Style(bgcolor=self.bgcolor))
            elif len(cell_ids) == 1:
                cell_idx = cell_ids[0]
                cell_value = cell_values[cell_idx]
                invert = cell_value < 0 and self._invertible()
                cell_style = Style(color=colors[cell_idx], bgcolor=self.bgcolor)
                if invert:
                    cell_style = invert_style(cell_style)
                yield Segment(
                    self.marks.get(cell_value, invert),
                    style=cell_style,
                )
            else:
                leading = max(cell_ids, key=lambda i: cell_values[i])
                trailing = min(cell_ids, key=lambda i: cell_values[i])
                if self.marks.invertible:
                    yield Segment(
                        self.marks.get(cell_values[trailing]),
                        style=Style(color=colors[trailing], bgcolor=colors[leading]),
                    )
                else:
                    if abs(cell_values[trailing]) > abs(cell_values[leading]):
                        cell_char = self.marks.get(1.0)
                        color = colors[trailing]
                        bgcolor = colors[leading]
                    else:
                        cell_char = self.marks.get(-1.0)
                        color = colors[leading]
                        bgcolor = colors[trailing]
                    cell_style = Style(
                        color=color,
                        bgcolor=bgcolor if self.marks.invertible else self.bgcolor,
                    )
                    yield Segment(cell_char, style=cell_style)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        for segment in self:
            yield segment

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, 1)


if __name__ == "__main__":
    from rich.console import Console
    from graphical.mark import (
        BAR_HEAVY_H,
        BAR_LIGHT_H,
        BAR_SHADE,
        WHISKER_HEAVY_H,
        WHISKER_LIGHT_H,
        WHISKER_DOUBLE_H,
        LOLLIPOP_FILLED_HEAVY_H,
        LOLLIPOP_FILLED_LIGHT_H,
        LOLLIPOP_OUTLINE_HEAVY_H,
        LOLLIPOP_OUTLINE_LIGHT_H,
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
        BAR_BLOCK_V,
        BAR_HEAVY_V,
        BAR_LIGHT_V,
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
            bars.append(
                StackedBar(
                    values=values,
                    value_range=(-120, 120),
                    width=width,
                    marks=markers,
                    colors=["green", "blue", "purple", "magenta", "yellow"],
                    bgcolor="black",
                    invert_negative=True,
                    orientation="vertical",
                )
            )

    for d in range(width):
        console.print(Segments([list(bar)[d] for bar in bars]))
        console.print()
