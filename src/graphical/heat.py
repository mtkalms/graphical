from typing import Optional, Tuple, Union

from rich.color import Color
from rich.console import Console, ConsoleOptions, RenderResult
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from graphical.bar import Orientation
from graphical.data import normalize
from graphical.scale.chromatic import SequentialScheme


class Heat:
    def __init__(
        self,
        data: Union[float, Tuple[float, float]],
        value_range: Tuple[float, float],
        scheme: SequentialScheme,
        *,
        orientation: Optional[Orientation] = None,
        repeat_x: Optional[int] = None,
        repeat_y: Optional[int] = None,
    ) -> None:
        self.data = data
        self.value_range = value_range
        self.scheme = scheme
        self.orientation = orientation or "horizontal"
        self.repeat_x = repeat_x
        self.repeat_y = repeat_y

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        data = self.data if isinstance(self.data, tuple) else [self.data]
        data = list(normalize(data, self.value_range))
        colors = [
            self.scheme.get(d) if d is not None else Color.default() for d in data
        ]
        for _ in range(self.repeat_y or 1):
            for _ in range(self.repeat_x or 1):
                if len(data) == 1:
                    yield Segment(" ", style=Style(bgcolor=colors[0]))
                elif self.orientation == "horizontal":
                    yield Segment("▌", style=Style(color=colors[0], bgcolor=colors[1]))
                else:
                    yield Segment("▄", style=Style(color=colors[1], bgcolor=colors[0]))
            if self.repeat_y:
                yield Segment.line()

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(1, 1)
