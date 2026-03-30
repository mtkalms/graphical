from typing import Iterable, Sequence, Tuple, TypeVar

T = TypeVar("T")


def pairs(data: Sequence[T]) -> Iterable[Tuple[T, T]]:
    return zip(data[::2], data[1::2])
