from typing import Generator, Sequence, Tuple


def normalize(
    data: Sequence[float],
    value_range: Tuple[float, float],
    clip: bool = True,
) -> Generator[float, None, None]:
    """Normalize ``data`` to ``value_range``.

    Args:
        data (Sequence[float]): Data to normalize.
        value_range (Tuple[float, float]): Value range to normalize to.
        clip (bool, optional): Clip out of range values. Defaults to True.

    Yields:
        Normalized data.
    """
    lower, upper = value_range
    for value in data:
        result = (value - lower) / (upper - lower)
        if clip:
            result = min(max(result, 0.0), 1.0)
        yield result
