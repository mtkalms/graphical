from itertools import zip_longest
import re
from typing import Literal, Optional
from tests.utilities.render import render_ansi

from rich.console import RenderableType, JustifyMethod, OverflowMethod
from rich.text import Text
from rich.style import Style

PreviewStyle = Literal["visual", "ansi", "markup"]


def _text_to_markup(text: Text) -> str:
    result = ""
    for span in text._spans:
        chars = text.plain[span.start : span.end]
        if span.style and span.style != Style.null():
            style = str(span.style)
            style = re.sub(r"\s?not \w+\s?", " ", style)
            result += f"[{style}]{chars}[/{style}]"
        else:
            result += chars
    return result


def assert_markup(
    renderable: RenderableType,
    markup: str,
    message: Optional[str] = None,
    preview: Optional[PreviewStyle] = None,
    justify: Optional[JustifyMethod] = None,
    overflow: Optional[OverflowMethod] = None,
    width: int = 80,
    no_wrap: Optional[bool] = None,
) -> None:
    rendered_a = render_ansi(
        renderable, justify=justify, overflow=overflow, width=width, no_wrap=no_wrap
    )
    rendered_b = render_ansi(Text.from_markup(markup, end=""), width=width)
    if preview:
        _preview_ansi(rendered_a, rendered_b, preview)
    assert rendered_a == rendered_b, message


def _preview_ansi(a: str, b: str, style: PreviewStyle):
    def cell_repr(c: str) -> str:
        if style == "ansi":
            return repr(c)
        if style == "markup":
            return _text_to_markup(Text.from_ansi(c))
        return c

    lines_a = a.splitlines(keepends=True)
    lines_b = b.splitlines(keepends=True)
    # Get max line length (without ANSI codes)
    print()
    print("Preview:")
    print(
        "\n".join(
            f"  actual: {cell_repr(a)}\n  expect: {cell_repr(b)}"
            for a, b in zip_longest(lines_a, lines_b)
        )
    )
