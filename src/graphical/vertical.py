from itertools import zip_longest, chain
from typing import Any, Iterable, List, Protocol, Union

from rich.console import Console, ConsoleOptions, RenderResult, RenderableType
from rich.measure import Measurement
from rich.segment import Segment


def _add_between(array: Iterable[Any], insert: Any) -> List[Any]:
    gapped = zip_longest(array, [insert] * (len(list(array)) - 1))
    return [d for d in chain.from_iterable(gapped) if d]


class VerticalRenderable(Protocol):
    def __vertical__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:  # pragma: no cover
        ...


class VerticalGroup:
    def __init__(self, *renderables: VerticalRenderable, gap: int = 0) -> None:
        self._renderables = renderables
        self._gap = gap

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
        for row in zip_longest(*rendered):
            if self._gap > 0:
                row = _add_between(row, Segment(" " * self._gap))
            yield from row
            yield Segment.line()
