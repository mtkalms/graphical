from rich.console import Console, ConsoleOptions, RenderResult, RenderableType
from rich.measure import Measurement
from rich.segment import Segment


class Offset:
    """Adds offset to renderable.

    Args:
        renderable (RenderableType): The renderable.
        x (int): Horizontal offset in number of cells.
        y (int): Vertical offset in number of cells.
    """

    def __init__(
        self,
        renderable: RenderableType,
        x: int,
        y: int,
    ) -> None:
        self._renderable = renderable
        self._offset_x = x
        self._offset_y = y

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        measurement = Measurement.get(console, options, self._renderable)
        return Measurement(*(m + self._offset_x for m in measurement))

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        new_line = Segment.line()
        for _ in range(self._offset_y):
            yield new_line
        for line in console.render_lines(self._renderable, pad=False):
            yield " " * self._offset_x
            yield from line
