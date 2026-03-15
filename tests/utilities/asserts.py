from itertools import zip_longest
from typing import Optional
from tests.utilities.render import render_ansi

from rich.console import RenderableType, JustifyMethod, OverflowMethod
from rich.text import Text


def assert_markup(
    renderable: RenderableType,
    markup: str,
    message: Optional[str] = None,
    preview: Optional[bool] = False,
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
        _preview_ansi(rendered_a, rendered_b)
    assert rendered_a == rendered_b, message


def _preview_ansi(a: str, b: str):
    lines_a = a.splitlines(keepends=True)
    lines_b = b.splitlines(keepends=True)
    # Get max line length (without ANSI codes)
    max_len = max(len(Text.from_ansi(a)) for a in lines_a)
    print()
    print("Preview:")
    print(
        "\n".join(
            f"{repr(a)}".ljust(max_len + 2) + f"\t{repr(b)}"
            for a, b in zip_longest(lines_a, lines_b)
        )
    )
