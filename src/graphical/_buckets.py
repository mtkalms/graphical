from typing import Callable, Generator, Sequence, TypeVar

Numeric = TypeVar("T", int, float)
SummaryFunction = Callable[[Sequence[Numeric]], float]


def buckets(
    values: Sequence[Numeric], count: int, summary_function: SummaryFunction
) -> Generator[float]:
    step = len(values) / count
    for d in range(count):
        segment = values[int(d * step) : int((d + 1) * step)]
        yield summary_function(segment)
