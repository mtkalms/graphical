from typing import Iterable, Sequence, Tuple, TypeVar

T = TypeVar("T")


def pairs(data: Sequence[T]) -> Iterable[Tuple[T, T]]:
    """Group data in pairs.

    Args:
        data (Sequence[T]): Data to group in pairs.

    Returns:
        Iterable[Tuple[T, T]]: Data in pairs
    """
    return zip(data[::2], data[1::2])
