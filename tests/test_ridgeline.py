from rich.box import HEAVY

from graphical.ridgeline import RidgelineChart
from graphical.sparkline import OneLinePlotStyle
from tests.util import render


class Test_RidgelineChart:
    def test_render(self):
        expected = (
            "                     Example RidgelineChart               \n"
            "      ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
            "row 1 ┫             ▁▁▁▁▁▁▁⎽⎽⎽⎽⎽⎽⎽⎼⎼⎼⎼⎼⎼⎼───────⎻⎻⎻⎻⎻⎻⎻⎺⎺┃\n"
            "row 2 ┫        ▁▁▁▁▁▁▁⎽⎽⎽⎽⎽⎽⎽⎼⎼⎼⎼⎼⎼⎼───────⎻⎻⎻⎻⎻⎻⎻⎺⎺⎺⎺⎺⎺⎺┃\n"
            "row 3 ┫   ▁▁▁▁▁▁▁⎽⎽⎽⎽⎽⎽⎽⎼⎼⎼⎼⎼⎼⎼───────⎻⎻⎻⎻⎻⎻⎻⎺⎺⎺⎺⎺⎺⎺▔    ┃\n"
            "      ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
            "       0                                               50\n"
        )
        chart = RidgelineChart(
            title="Example RidgelineChart",
            value_range=(0, 10),
            plot_style=OneLinePlotStyle.LINE,
            box=HEAVY,
            ticks=(0, 50),
        )
        chart.add_row(label="row 1", values=[-1 + d / 5 for d in range(50)])
        chart.add_row(label="row 2", values=[d / 5 for d in range(50)])
        chart.add_row(label="row 3", values=[1 + d / 5 for d in range(50)])
        assert render(chart) == expected
