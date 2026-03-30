from typing import List, Optional, Sequence, Tuple
from graphical.data._normalize import normalize


def bands(
    data: Sequence[float],
    num_bands: int,
    value_range: Optional[Tuple[float, float]] = None,
) -> List[Tuple[int, float]]:
    """Split data into bands.

    Args:
        data (Sequence[float]): Data to split into bands.
        num_bands (int): Number of bands.
        value_range (Tuple[float, float], optional): Lower and upper boundary. Defaults to range of data.

    Returns:
        List[Tuple[int, float]]: List of tuples (band index, value).
    """
    value_range = value_range or (min(data), max(data))
    normalized = normalize(data, value_range)
    return [(int(d * num_bands), (d * num_bands) % 1.0) for d in normalized]
