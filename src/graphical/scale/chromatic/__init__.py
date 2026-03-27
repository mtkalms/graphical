from math import floor
from typing import List
from rich.color import Color


def _spline(t: float, p0: float, p1: float, p2: float, p3: float) -> float:
    """Calculates a cubic B-spline point for a given t [0, 1]."""
    t = max(0.0, min(1.0, t))
    b0 = ((1 - t) ** 3) / 6
    b1 = (3 * t**3 - 6 * t**2 + 4) / 6
    b2 = (-3 * t**3 + 3 * t**2 + 3 * t + 1) / 6
    b3 = (t**3) / 6
    return b0 * p0 + b1 * p1 + b2 * p2 + b3 * p3


def _interpolate(t: float, *values: float) -> float:
    t = max(0.0, min(1.0, t))
    n = len(values) - 1
    i = floor(t * n)
    p1 = values[i]
    p2 = values[i + 1]
    # Edge behaviour: Add additional value with similar spacing
    p0 = values[i - 1] if i > 0 else 2 * p1 - p2
    p3 = values[i + 2] if i < (n - 1) else 2 * p2 - p1
    return _spline(t, p0, p1, p2, p3)


def _interpolate_closed(t: float, *values: float) -> float:
    n = len(values) - 1
    i = floor(t * n)
    p0 = values[(i - 1) % n]
    p1 = values[i % n]
    p2 = values[(i + 1) % n]
    p3 = values[(i + 2) % n]
    return _spline(t, p0, p1, p2, p3)


class SequentialScheme:
    def __init__(self, *colors: str, closed: bool = False) -> None:
        self._colors = [Color.parse(c) for c in colors]
        self._closed = closed

    def get(self, value: float) -> Color:
        interpolate = _interpolate_closed if self._closed else _interpolate
        triplets = [[*c.get_truecolor()] for c in self._colors]
        channels = zip(*triplets)
        rgb_value = [interpolate(value, *channel) for channel in channels]
        return Color.from_rgb(*rgb_value)

    @property
    def colors(self) -> List[Color]:
        return self._colors[:]

    def palette(self, n: int) -> List[Color]:
        return [self.get(d / (n - 1)) for d in range(n)]


class OrdinalScheme:
    def __init__(self, *colors: str, closed: bool = True) -> None:
        self._colors = [Color.parse(c) for c in colors]
        self._closed = closed

    def get(self, value: int) -> Color:
        if self._closed:
            value = max(0, min(len(self._colors) - 1, value))
        else:
            value = value % (len(self._colors) - 1)
        return self._colors[value]

    @property
    def colors(self) -> List[Color]:
        return self._colors[:]
