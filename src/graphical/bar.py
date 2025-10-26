import math

from typing import Tuple, Optional, TypeVar

from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.segment import Segment
from rich.measure import Measurement
from rich.style import Style


from graphical.mark import *
from graphical.section import Section

T = TypeVar("T", int, float)


class Bar:

    def __init__(
        self,
        value: T,
        value_range: Tuple[T, T],
        width: int,
        cells: Optional[Mark] = BAR_BLOCK_H,
        color: Optional[Color] = None,
        bgcolor: Optional[Color] = None,
        invert_negative: bool = False,
    ) -> None:
        self.value = value
        self.value_range = value_range
        self.width = width
        self.cells = cells
        self.color = color
        self.bgcolor = bgcolor
        self.invert_negative = invert_negative

    @classmethod
    def _cell_value(cls, bar: Section, segment: Section) -> float:
        intersection = segment.intersect(bar)
        if not intersection:
            return 0.0
        elif segment == intersection:
            return 1.0
        else:
            sign = 1.0 if intersection.middle < segment.middle else -1.0
            return sign * intersection.length / segment.length

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        style = Style(color=self.color, bgcolor=self.bgcolor)
        inverse_style = Style(color=self.bgcolor, bgcolor=self.color)
        bar = Section(min(0, self.value), max(0, self.value))
        for segment in Section(*self.value_range).segment(self.width):
            cell_value = self._cell_value(bar, segment)
            # Handle origin that falls between segment boundaries
            if segment.lower < 0.0 < segment.upper:
                if self.value in segment:
                    cell_value = 0.0
                else:
                    cell_value = math.copysign(0.5, cell_value)
            invert = (
                cell_value < 0
                and self.invert_negative
                and self.color not in [None, "default"]
                and self.bgcolor not in [None, "default"]
                and self.cells.invertible
            )
            cell_style = inverse_style if invert else style
            if self.value in segment and self.value != segment.lower:
                cell_char = self.cells.cap(cell_value, invert)
            else:
                cell_char = self.cells.get(cell_value, invert)
            yield Segment(cell_char, style=cell_style)

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, 1)


if __name__ == "__main__":
    from rich.console import Console

    console = Console()

    for row_value in range(-20, 21):
        for markers in [
            BAR_BLOCK_H,
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
        ]:
            console.print(
                Bar(
                    value=row_value / 4.3,
                    value_range=(-5.1, 5.1),
                    width=10,
                    cells=markers,
                    # color="red",
                    # bgcolor="black",
                    invert_negative=True,
                )
            )
        print(f"\t{row_value / 4.3}")
