from click import Tuple


class Mark:
    """Defines the range of characters to render a mark."""

    def __init__(
        self,
        positive: str,
        negative: str = None,
        caps: str | Tuple[str, str] = None,
        invertible: bool = False,
    ):
        """Initialize mark chars.

        Args:
            positive (str): Mark chars for positive value.
            negative (str, optional): Mark chars for negative values. Defaults to positive.

        """
        self._positive = positive
        self._negative = negative or positive
        if isinstance(caps, str):
            self._caps = (caps, caps)
        else:
            self._caps = caps
        self._invertible = invertible

    @property
    def invertible(self):
        return self._invertible

    def cap(self, value: float, invert: bool = False) -> str:
        if self._caps:
            return self._caps[0] if value > 0 else self._caps[1]
        else:
            return self.get(value, invert)

    def get(self, value: float, invert: bool = False) -> str:
        """Maps a value in the domain [-1, 1] to the correpsonding character.

        Args:
            value (float): Value in the domain [-1, 1].
            invert (bool, optional): Get inverted character. Defaults to False.

        Raises:
            ValueError: Value must be in domain [-1.0, 1.0].

        Returns:
            str: Character representing the value.
        """
        if abs(value) > 1:
            raise ValueError("Value must be normalized to domain [-1.0, 1.0].")
        if invert:
            return self.get(1 - abs(value), False)
        mark_chars = self._positive if value >= 0 else self._negative
        mark_index = int(round(abs(value) * (len(mark_chars) - 1)))
        return mark_chars[mark_index]


BAR_BLOCK_H = Mark(" ▏▎▍▌▋▊▉█", " ▕▐█", invertible=True)
BAR_BLOCK_V = Mark(" ▁▂▃▄▅▆▇█" " ▔▀█", invertible=True)
BAR_LIGHT_H = Mark(" ╴─", " ╶─")
BAR_LIGHT_V = Mark(" ╷│", " ╵│")
BAR_HEAVY_H = Mark(" ╸━", " ╺━")
BAR_HEAVY_V = Mark(" ╻┃", " ╹┃")
BAR_SHADE = Mark(" ░▒▓█")

WHISKER_LIGHT_H = Mark(" ─", caps=("┤", "├"))
WHISKER_HEAVY_H = Mark(" ━", caps=("┫", "┣"))
WHISKER_DOUBLE_H = Mark(" ═", caps=("╣", "╠"))

LOLLIPOP_OUTLINE_LIGHT_H = Mark(" ─", caps="◯")
LOLLIPOP_OUTLINE_HEAVY_H = Mark(" ━", caps="◯")
LOLLIPOP_FILLED_LIGHT_H = Mark(" ─", caps="●")
LOLLIPOP_FILLED_HEAVY_H = Mark(" ━", caps="●")
