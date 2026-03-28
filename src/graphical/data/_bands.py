from typing import List, Optional, Sequence, Tuple
from graphical.data._normalize import normalize


def bands(
    data: Sequence[float],
    n: int,
    value_range: Optional[Tuple[float, float]] = None,
) -> List[Tuple[int, float]]:
    value_range = value_range or (min(data), max(data))
    normalized = normalize(data, value_range)
    return [(int(d * n), (d * n) % 1.0) for d in normalized]
