import pytest

from graphical.sparkline import OneLinePlotStyle, Sparkline

from .util import render


@pytest.mark.parametrize(
    "plot_style, width, expected",
    [
        (OneLinePlotStyle.LINE, 8, "  ▁⎽⎼─⎻⎺▔ "),
        (OneLinePlotStyle.AREA, 9, "  ▁▂▃▄▅▆▇██"),
        (OneLinePlotStyle.HORIZON, 18, "   ▁▂▃▄▅▆▇ ▁▂▃▄▅▆▇██"),
        (OneLinePlotStyle.SHADE, 5, "  ░▒▓██"),
    ],
)
def test_ascending_pattern(plot_style: OneLinePlotStyle, width: int, expected: str):
    chart = Sparkline(
        values=[-1 + d for d in range(width + 2)],
        value_range=(0, width - 1),
        plot_style=plot_style,
        end="",
    )
    assert render(chart) == expected


@pytest.mark.parametrize(
    "plot_style, width, expected",
    [
        (OneLinePlotStyle.LINE, 8, "  ▔⎺⎻─⎼⎽▁ "),
        (OneLinePlotStyle.AREA, 9, "███▇▆▅▄▃▂▁ "),
        (OneLinePlotStyle.HORIZON, 18, "███▇▆▅▄▃▂▁ ▇▆▅▄▃▂▁  "),
        (OneLinePlotStyle.SHADE, 5, "███▓▒░ "),
    ],
)
def test_descending_pattern(plot_style: OneLinePlotStyle, width: int, expected: str):
    chart = Sparkline(
        values=[width + 1 - d for d in range(width + 2)],
        value_range=(0, width - 1),
        plot_style=plot_style,
        end="",
    )
    assert render(chart) == expected
