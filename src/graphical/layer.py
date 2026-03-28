from itertools import zip_longest
from typing import Callable, List, Optional

from rich.console import Console, ConsoleOptions, RenderResult, RenderableType
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style


BlendFunction = Callable[[Segment, Segment], Segment]


def _segments(
    renderable: RenderableType, console: Console, options: ConsoleOptions
) -> List[List[Segment]]:
    result = []
    lines = console.render_lines(
        renderable,
        options,
        pad=False,
    )
    for line in lines:
        _line = []
        for segment in line:
            _line += [*(Segment(s, segment.style) for s in segment.text)]
        result.append(_line)
    return result


def _blend(a: Segment, b: Segment) -> Segment:
    if b.text != " ":
        style = (a.style or Style.null()) + (b.style or Style(color="default"))
        return Segment(b.text, style)
    if b.style and b.style.bgcolor and b.style.bgcolor != "default":
        return b
    return a


class Layers:
    """Stacks and blends renderables as layers.

    Args:
        *renderables (RenderableType): Renderables to be stacked.
        blend (BlendFunction, optional): Function that defines how two one-cell segments are blended.
    """

    def __init__(
        self,
        *renderables: RenderableType,
        blend: Optional[BlendFunction] = None,
    ) -> None:
        self._renderables = renderables
        self._blend = blend or _blend

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
        rendered = [_segments(r, console, options) for r in self._renderables]
        for lines in zip_longest(*rendered, fillvalue=[]):
            segments = []
            for cells in [d for d in zip_longest(*lines)]:
                segment = Segment(" ")
                for cell in [d for d in cells if d]:
                    segment = self._blend(segment, cell)
                segments.append(segment)
            yield from Segment.simplify(segments)
            yield Segment.line()


if __name__ == "__main__":
    from graphical.bar import Stack
    from rich.text import Text

    console = Console()
    bar = Stack((50, 25, 12), (0, 87), prefer_bg="all")
    text = Text("abcdefghijklmnopqrstuvw.", justify="left")
    console.print(Layers(bar, text))
