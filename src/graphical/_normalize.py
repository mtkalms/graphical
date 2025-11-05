from typing import Tuple, Union

Numeric = Union[int, float]


def normalize(value: Numeric, value_range: Tuple[Numeric, Numeric]) -> float:
    result = (value - value_range[0]) / (value_range[1] - value_range[0])
    return min(max(result, 0.0), 1.0)
