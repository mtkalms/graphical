from typing import Callable, Iterable, Sequence, Union

Numeric = Union[int, float]
SummaryFunction = Callable[[Sequence[Numeric]], float]


def buckets(
    values: Sequence[Numeric],
    count: int,
    summary_function: SummaryFunction,
    stretch: bool = True,
) -> Iterable[Sequence[Numeric]]:
    step = len(values) / count
    for d in range(count):
        lower = int(d * step)
        upper = int((d + 1) * step)
        if stretch:
            upper = max(upper, lower + 1)
        segment = values[lower:upper]
        yield summary_function(segment)
