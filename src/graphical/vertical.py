from itertools import zip_longest
from typing import Iterable, List, Protocol, Union

from rich.console import Console, ConsoleOptions, RenderResult, RenderableType
from rich.measure import Measurement
from rich.segment import Segment


class VerticalRenderable(Protocol):
    def __vertical__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:  # pragma: no cover
        ...


class VerticalGroup:
    def __init__(self, *renderables: VerticalRenderable) -> None:
        self._renderables: Iterable[VerticalRenderable] = renderables

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(options.max_width, options.max_width)

    def render_columns(
        self, console: Console, options: ConsoleOptions
    ) -> List[List[Union[RenderableType, Segment]]]:
        return [list(d.__vertical__(console, options)) for d in self._renderables]

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        rendered = self.render_columns(console, options)
        for line in zip_longest(*rendered):
            yield from line
            yield Segment.line()
