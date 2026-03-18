from itertools import zip_longest, chain
from typing import Any, Iterable, List, Protocol

from rich.console import Console, ConsoleOptions, RenderResult
from rich.measure import Measurement
from rich.segment import Segment


def _add_between(array: Iterable[Any], insert: Any) -> List[Any]:
    gapped = zip_longest(array, [insert] * (len(list(array)) - 1))
    return [d for d in chain.from_iterable(gapped) if d]


class GroupRenderable(Protocol):
    def __graphical_group__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:  # pragma: no cover
        ...


class Horizontal:
    """Arranges renderables horizontally.
    All renderables need to implement the `GroupRenderable` protocol.

    Args:
        *renderables (GroupRenderable): Renderables to be arranged horizontally.
        gap (int, optional): Gap between renderables. Defaults to 0.
    """

    def __init__(self, *renderables: GroupRenderable, gap: int = 0) -> None:
        self._renderables = renderables
        self._gap = gap

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(options.max_width, options.max_width)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        rendered = [
            list(d.__graphical_group__(console, options)) for d in self._renderables
        ]
        for row in zip_longest(*rendered):
            if self._gap > 0:
                row = _add_between(row, Segment(" " * self._gap))
            yield from row
            yield Segment.line()
