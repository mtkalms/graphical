import io

from rich.console import Console, RenderableType


def render(renderable: RenderableType) -> str:
    console = Console(file=io.StringIO(), legacy_windows=False, width=256)
    console.print(renderable, no_wrap=True)
    return console.file.getvalue()
