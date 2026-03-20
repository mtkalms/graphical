from typing import Optional
from rich.console import Console
from rich.text import Text


class MarkupResult(str):
    def __new__(cls, *lines) -> "MarkupResult":
        return super().__new__(cls, "\n".join(lines) if lines else "")

    def preview(self, console: Optional[Console] = None, width: Optional[int] = 256):
        _console = console or Console(width=width)
        _console.print(Text.from_markup("\n" + self))
