from typing import List

import pytest
from rich.box import HEAVY

from graphical.bar import (
    Bar,
    BarStyle,
    BarChart,
    DivergingBar,
    StackedBar,
    DoubleBar,
    DivergingBarChart,
    StackedBarChart,
    DoubleBarChart,
)
from tests.util import render


class Test_Bar:
    @pytest.mark.parametrize(
        "value, bar_style, expected",
        [
            (0.0, BarStyle.BLOCK, "                    "),
            (9.5, BarStyle.BLOCK, "███████████████████ "),
            (5.2, BarStyle.BLOCK, "██████████▍         "),
            (5.2, BarStyle.HEAVY, "━━━━━━━━━━╸         "),
            (5.2, BarStyle.LIGHT, "──────────╴         "),
            (5.2, BarStyle.SHADE, "██████████▒         "),
        ],
        ids=[
            "BLOCK_none",
            "BLOCK_full",
            "BLOCK_partial",
            "HEAVY_partial",
            "LIGHT_partial",
            "SHADE_partial",
        ],
    )
    def test_render(self, value: float, bar_style: BarStyle, expected: str):
        chart = Bar(
            value=value,
            value_range=(0, 10),
            width=20,
            bar_style=bar_style,
            end="",
        )
        assert render(chart) == expected


class Test_DivergingBar:
    @pytest.mark.parametrize(
        "value, bar_style, expected",
        [
            (+0.0, BarStyle.BLOCK, "                    "),
            (+9.5, BarStyle.BLOCK, "          █████████▌"),
            (-9.5, BarStyle.BLOCK, "▐█████████          "),
            (+5.3, BarStyle.BLOCK, "          █████▎    "),
            (-5.3, BarStyle.BLOCK, "    ▕█████          "),
            (+5.3, BarStyle.HEAVY, "          ━━━━━╸    "),
            (-5.3, BarStyle.HEAVY, "    ╺━━━━━          "),
            (+5.3, BarStyle.LIGHT, "          ─────╴    "),
            (-5.3, BarStyle.LIGHT, "    ╶─────          "),
            (+5.3, BarStyle.SHADE, "          █████░    "),
            (-5.3, BarStyle.SHADE, "    ░█████          "),
        ],
        ids=[
            "BLOCK_none",
            "BLOCK_positive",
            "BLOCK_negative",
            "BLOCK_positive_partial",
            "BLOCK_negative_partial",
            "HEAVY_positive_partial",
            "HEAVY_negative_partial",
            "LIGHT_positive_partial",
            "LIGHT_negative_partial",
            "SHADE_positive_partial",
            "SHADE_negative_partial",
        ],
    )
    def test_render(self, value: float, bar_style: BarStyle, expected: str):
        chart = DivergingBar(
            value=value,
            value_range=(-10, 10),
            width=20,
            bar_style=bar_style,
            end="",
        )
        assert render(chart) == expected


class Test_StackedBar:
    @pytest.mark.parametrize(
        "values, bar_style, expected",
        [
            ([0.0, 5.2], BarStyle.BLOCK, " █████████▍         "),
            ([5.2, 4.5], BarStyle.BLOCK, "██████████▍████████▍"),
            ([5.2, 0.8], BarStyle.BLOCK, "██████████▍█        "),
        ],
        ids=["short+medium", "medium+medium", "medium+short"],
    )
    def test_render(self, values: List[float], bar_style: BarStyle, expected: str):
        chart = StackedBar(
            values=values,
            value_range=(0, 10),
            width=20,
            end="",
            colors=["purple", "blue"],
        )
        assert render(chart) == expected


class Test_DoubleBar:
    @pytest.mark.parametrize(
        "values, bar_style, expected",
        [
            ([0.0, 5.2], BarStyle.BLOCK, "▄▄▄▄▄▄▄▄▄▄▄         "),
            ([5.2, 9.5], BarStyle.BLOCK, "▀▀▀▀▀▀▀▀▀▀▀▄▄▄▄▄▄▄  "),
            ([5.2, 6.8], BarStyle.BLOCK, "▀▀▀▀▀▀▀▀▀▀▀▄▄▄      "),
            ([6.8, 5.2], BarStyle.BLOCK, "▀▀▀▀▀▀▀▀▀▀▀▀▀▀      "),
        ],
        ids=["short+medium", "medium+long", "medium+medium", "long+medium"],
    )
    def test_render(self, values: List[float], bar_style: BarStyle, expected: str):
        chart = DoubleBar(
            values=values,
            value_range=(0, 10),
            width=20,
            end="",
            colors=["purple", "blue"],
        )
        assert render(chart) == expected


class Test_BarChart:
    def test_render(self):
        expected = (
            "                    Example BarChart              \n"
            "       ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
            " first ┫████████████████████▌                    ┃\n"
            "second ┫█████████████████████████████████████████┃\n"
            " third ┫████▏                                    ┃\n"
            "       ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
            "        0                                      10\n"
        )
        chart = BarChart(
            title="Example BarChart",
            value_range=(0, 10),
            width=50,
            box=HEAVY,
        )
        chart.add_row(label="first", value=5.0)
        chart.add_row(label="second", value=10)
        chart.add_row(label="third", value=1.0)
        assert render(chart) == expected


class Test_DivergingBarChart:
    def test_render(self):
        expected = (
            "               Example DivergingBarChart         \n"
            "       ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
            " first ┫                    ██████████          ┃\n"
            "second ┫                                        ┃\n"
            " third ┫       ▕████████████                    ┃\n"
            "       ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
            "        -10                                   10\n"
        )
        chart = DivergingBarChart(
            title="Example DivergingBarChart",
            value_range=(-10, 10),
            width=50,
            box=HEAVY,
        )
        chart.add_row(label="first", value=5.0)
        chart.add_row(label="second", value=0.0)
        chart.add_row(label="third", value=-6.1)
        assert render(chart) == expected


class Test_StackedBarChart:
    def test_render(self):
        expected = (
            "                 Example StackedBarChart          \n"
            "       ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
            " first ┫████████▎                                ┃\n"
            "second ┫ ███████████████████▌                    ┃\n"
            " third ┫████████████▎███████████████████▊        ┃\n"
            "       ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
            "        0                                      10\n"
        )
        chart = StackedBarChart(
            title="Example StackedBarChart",
            colors=["purple", "red"],
            value_range=(0, 10),
            width=50,
            box=HEAVY,
        )
        chart.add_row(label="first", values=[2.0, 0.0])
        chart.add_row(label="second", values=[0.0, 5.0])
        chart.add_row(label="third", values=[3.0, 5.0])
        assert render(chart) == expected


class Test_DoubleBarChart:
    def test_render(self):
        expected = (
            "                 Example DoubleBarChart           \n"
            "       ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
            " first ┫▀▀▀▀▀▀▀▀▀                                ┃\n"
            "second ┫▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                    ┃\n"
            " third ┫▀▀▀▀▀▀▀▀▀▀▀▀▀▄▄▄▄▄▄▄▄                    ┃\n"
            "       ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
            "        0                                      10\n"
        )
        chart = DoubleBarChart(
            title="Example DoubleBarChart",
            colors=["purple", "red"],
            value_range=(0, 10),
            width=50,
            box=HEAVY,
        )
        chart.add_row(label="first", values=[2.0, 0.0])
        chart.add_row(label="second", values=[0.0, 5.0])
        chart.add_row(label="third", values=[3.0, 5.0])
        assert render(chart) == expected
