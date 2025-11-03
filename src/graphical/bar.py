import math

from typing import Sequence, Tuple, Optional, TypeVar

from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.segment import Segment
from rich.measure import Measurement
from rich.style import Style


from graphical._invert_style import invert_style
from graphical.mark import Mark, BAR_BLOCK_H
from graphical.section import Section

Numeric = TypeVar("T", int, float)


class Bar:
    def __init__(
        self,
        value: Numeric,
        value_range: Tuple[Numeric, Numeric],
        width: int,
        marks: Optional[Mark] = BAR_BLOCK_H,
        color: Optional[Color] = None,
        bgcolor: Optional[Color] = None,
        invert_negative: bool = False,
    ) -> None:
        self.value = value
        self.value_range = value_range
        self.width = width
        self.marks = marks
        self.color = color
        self.bgcolor = bgcolor
        self.invert_negative = invert_negative

    @classmethod
    def _cell_value(cls, bar: Section, segment: Section) -> float:
        intersection = segment.intersect(bar)
        if not intersection:
            return 0.0
        elif segment == intersection:
            return -1.0 if bar.lower < 0 else 1.0
        else:
            sign = 1.0 if intersection.middle < segment.middle else -1.0
            return sign * intersection.length / segment.length

    def _invertible(self) -> bool:
        return (
            self.invert_negative
            and self.color not in [None, "default"]
            and self.bgcolor not in [None, "default"]
            and self.marks.invertible
        )

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        style = Style(color=self.color, bgcolor=self.bgcolor)
        bar = Section(min(0, self.value), max(0, self.value))
        for segment in Section(*self.value_range).segment(self.width):
            cell_value = self._cell_value(bar, segment)
            # Handle origin that falls between segment boundaries
            if segment.lower < 0.0 < segment.upper:
                if self.value in segment:
                    cell_value = 0.0
                else:
                    cell_value = math.copysign(0.5, cell_value)
            invert = cell_value < 0 and self._invertible()
            cell_style = invert_style(style) if invert else style
            if self.value in segment and self.value != segment.lower:
                # Use cap character for the upper boundary of the bar
                cell_char = self.marks.cap(cell_value, invert)
            else:
                cell_char = self.marks.get(cell_value, invert)
            yield Segment(cell_char, style=cell_style)

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
        marks: Optional[Mark] = BAR_BLOCK_H,
        colors: Sequence[Color] = ["red", "green", "blue", "yellow"],
        bgcolor: Optional[Color] = None,
    ) -> None:
        self.values = values
        self.value_range = value_range
        self.width = width
        self.marks = marks
        self.colors = colors
        self.bgcolor = bgcolor

    @classmethod
    def _cell_value(cls, bar: Section, segment: Section) -> float:
        intersection = segment.intersect(bar)
        if not intersection:
            cell_value = 0.0
        elif segment == intersection:
            sign = -1.0 if bar.lower < 0 else 1.0
            cell_value = sign * 1.0
        else:
            sign = 1.0 if intersection.middle < segment.middle else -1.0
            if segment.lower < 0.0 < segment.upper:
                cell_value = 0.0 if bar in segment else sign * 0.5
            else:
                cell_value = sign * intersection.length / segment.length
        return cell_value

    def stacked_colors(self) -> Sequence[Color]:
        colors = []
        for idx, value in enumerate(self.values):
            if value >= 0:
                colors.append(self.colors[idx % len(self.colors)])
            else:
                colors.insert(0, self.colors[idx % len(self.colors)])
        return colors

    def stacked_bars(self) -> Sequence[Numeric]:
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

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        colors = self.stacked_colors()
        bars = self.stacked_bars()
        for segment in Section(*self.value_range).segment(self.width):
            cell_values = [self._cell_value(bar, segment) for bar in bars]
            # Handle origin that falls between segment boundaries
            end_idx = None
            cell_char = self.marks.get(0.0)
            cell_color = None
            cell_bgcolor = self.bgcolor
            for idx, cell_value in enumerate(cell_values):
                if abs(cell_value) == 1.0:
                    cell_char = self.marks.get(cell_value)
                    cell_color = colors[idx]
                    break
                elif cell_value > 0.0:
                    end_idx = idx
                    cell_char = self.marks.get(cell_values[idx])
                    cell_color = colors[idx]
                elif cell_value < 0.0:
                    if end_idx is not None:
                        cell_bgcolor = colors[idx]
                    else:
                        cell_char = self.marks.get(cell_values[idx])
                        cell_color = colors[idx]
                    break
            yield Segment(
                cell_char, style=Style(color=cell_color, bgcolor=cell_bgcolor)
            )

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
    )

    console = Console()

    for values in [
        [20, 25, 30, 35],
        [15, 20, 10, 25],
        [10, 15, 12, 18],
        [12, 10, 15, 11],
        [20, -25, 30, -35],
        [15, -20, 10, 25],
        [10, 15, -12, 18],
        [12, 10, 15, -11],
        [-20, -25, -30, -35],
        [-15, -20, -10, -25],
        [-10, -15, -12, -18],
        [-12, -10, -15, -11],
    ]:
        console.print(
            StackedBar(
                values=values,
                value_range=(-130, 120),
                width=44,
                marks=BAR_BLOCK_H,
                colors=["green", "blue", "purple", "magenta"],
            )
        )
        console.print()
        console.print()
