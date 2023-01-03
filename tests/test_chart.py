from rich.box import HEAVY
from rich.console import RenderResult, ConsoleOptions, Console
from rich.segment import Segment

from graphical.chart import LabelChartRenderer
from tests.util import render


class RenderWrapper:
    def __init__(self, renderer: LabelChartRenderer):
        self.renderer = renderer

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield from self.renderer.render()


class Test_LabelChartRenderer:
    def test_render(self):
        expected = (
            "             Test Chart       \n"
            "       ┏━━━━━━━━━━━━━━━━━━━━━┓\n"
            " first ┫▁▂▃▅▆▆▅▄▂▁▁▂▃▅▆▆▅▄▂▁ ┃\n"
            "       ┫Spacer               ┃\n"
            "second ┫▁▂▃▅▆▆▅▄▂▁▁▂▃▅▆▆▅▄▂▁ ┃\n"
            "       ┗━━━━━━━━━━━━━━━━━━━━━┛\n"
            "        0                  10\n"
        )

        chart = LabelChartRenderer(title="Test Chart", ticks=(0, 10), box=HEAVY)
        chart.add_row(
            label="first",
            content_width=20,
            content="▁▂▃▅▆▆▅▄▂▁▁▂▃▅▆▆▅▄▂▁",
        )
        chart.add_row(
            label=" ",
            content_width=6,
            content="Spacer",
        )
        chart.add_row(
            label="second",
            content_width=21,
            content=Segment("▁▂▃▅▆▆▅▄▂▁▁▂▃▅▆▆▅▄▂▁ "),
        )
        assert render(RenderWrapper(chart)) == expected
