import io
from typing import Optional
from rich.console import Console, RenderableType, JustifyMethod, OverflowMethod


def render_ansi(
    renderable: RenderableType,
    width: Optional[int] = 80,
    no_wrap: Optional[bool] = False,
    justify: Optional[JustifyMethod] = None,
    overflow: Optional[OverflowMethod] = None,
) -> str:
    file = io.StringIO()
    console = Console(file=file, legacy_windows=False, width=width, record=True)
    console.print(
        renderable, no_wrap=no_wrap, justify=justify, overflow=overflow, end=""
    )
    return console.export_text(styles=True)
