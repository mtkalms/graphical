from typing import Literal, Optional

from rich.style import Style

InversionStrategy = Literal[
    "reverse",  # Use reverse ANSI code
    "swap",  # Swap color and bgcolor
]


def invert_style(style: Style, strategy: Optional[InversionStrategy] = "swap") -> Style:
    """Invert a Rich Style by swapping its foreground and background colors.

    Args:
        style (Style): The original style to invert.
    Returns:
        Style: The inverted style.
    """
    match strategy:
        case "swap":
            return style + Style(color=style.bgcolor, bgcolor=style.color)
        case "reverse":
            return style + Style(reverse=True)
        case _:
            return style
