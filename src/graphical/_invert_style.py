from rich.style import Style


def invert_style(style: Style) -> Style:
    """Invert a Rich Style by swapping its foreground and background colors.

    Args:
        style (Style): The original style to invert.
    Returns:
        Style: The inverted style.
    """
    return Style(color=style.bgcolor, bgcolor=style.color)
