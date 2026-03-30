from typing import Optional

from rich.style import Style

from graphical.options import InversionStrategy


def invert_style(style: Style, strategy: Optional[InversionStrategy] = "swap") -> Style:
    """Invert a Rich Style by swapping its foreground and background colors.

    Args:
        style (Style): The original style to invert.
    Returns:
        Style: The inverted style.
    """
    if strategy == "swap":
        return style + Style(color=style.bgcolor, bgcolor=style.color)
    if strategy == "reverse":
        return style + Style(reverse=True)
    return style
