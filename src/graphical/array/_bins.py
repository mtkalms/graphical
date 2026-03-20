from statistics import mean
from typing import Callable, Generator, Sequence, Union

Numeric = Union[int, float]
SummaryFunction = Callable[[Sequence[Numeric]], float]


def bins(
    data: Sequence[Numeric],
    num_bins: int,
    *,
    summary_function: SummaryFunction = mean,
    spread: bool = True,
) -> Generator[float, None, None]:
    """Resample ``data`` into ``num_bins`` bins.

    Args:
        data (Sequence[Numeric]): Data to resample.
        num_bins (int): Number of bins
        summary_function (SummaryFunction): Function to summarize the data in each bin. Defaults to ``mean``.
        spread (bool, optional): Fill in values if ``num_bins > len(data)``. Defaults to True.

    Yields:
        Binned data.
    """
    step = len(data) / num_bins
    for d in range(num_bins):
        lower = int(d * step)
        upper = int((d + 1) * step)
        if spread:
            upper = max(upper, lower + 1)
        segment = data[lower:upper]
        yield summary_function(segment)
