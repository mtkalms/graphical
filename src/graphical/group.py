from itertools import zip_longest

from rich.console import Console, ConsoleOptions, RenderResult, RenderableType
from rich.measure import Measurement
from rich.segment import Segment


class Horizontal:
    """Arranges renderables horizontally.

    Args:
        *renderables (RenderableType): Renderables to be arranged.
        gap (int, optional): Gap between renderables. Defaults to 0.
    """

    def __init__(self, *renderables: RenderableType, gap: int = 0) -> None:
        self._renderables = renderables
        self._gap = gap

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        mins = []
        maxs = []
        for renderable in self._renderables:
            _min, _max = Measurement.get(console, options, renderable)
            mins.append(_min)
            maxs.append(_max)
        return Measurement(sum(mins), sum(maxs))

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        new_line = Segment.line()
        rendered = [console.render_lines(d, pad=False) for d in self._renderables]
        for row_idx, row in enumerate(zip_longest(*rendered)):
            if row_idx > 0:
                yield new_line
            for col_idx, cell in enumerate(row):
                if col_idx > 0 and self._gap > 0:
                    yield Segment(" " * self._gap)
                if cell is not None:
                    yield from cell


class Vertical:
    """Arranges renderables vertically.

    Args:
        *renderables (RenderableType): Renderables to be arranged.
        gap (int, optional): Gap between renderables. Defaults to 0.
    """

    def __init__(self, *renderables: RenderableType, gap: int = 0) -> None:
        self._renderables = renderables
        self._gap = gap

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        mins = []
        maxs = []
        for renderable in self._renderables:
            _min, _max = Measurement.get(console, options, renderable)
            mins.append(_min)
            maxs.append(_max)
        return Measurement(max(mins), max(maxs))

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        new_line = Segment.line()
        for row_idx, renderable in enumerate(self._renderables):
            if row_idx > 0 and self._gap > 0:
                yield from [new_line] * self._gap
            yield renderable
            yield new_line
