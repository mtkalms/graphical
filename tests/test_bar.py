from typing import List

import pytest
from graphical.bar import Bar
from graphical.mark import *
from tests.util import render


class Test_Bar:
    @pytest.mark.parametrize(
        "value, cells, expected",
        [
            (0.0, BAR_BLOCK_H, "                    "),
            (9.5, BAR_BLOCK_H, "███████████████████ "),
            (5.2, BAR_BLOCK_H, "██████████▍         "),
            (5.2, BAR_HEAVY_H, "━━━━━━━━━━╸         "),
            (5.2, BAR_LIGHT_H, "──────────╴         "),
            (5.2, BAR_SHADE, "██████████▒         "),
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
    def test_render(self, value: float, cells: Mark, expected: str):
        chart = Bar(
            value=value,
            value_range=(0, 10),
            width=20,
            marks=cells,
        )
        assert render(chart) == expected


class Test_DivergingBar:
    @pytest.mark.parametrize(
        "value, cells, expected",
        [
            (+0.0, BAR_BLOCK_H, "                    "),
            (+9.5, BAR_BLOCK_H, "          █████████▌"),
            (-9.5, BAR_BLOCK_H, "▐█████████          "),
            (+5.3, BAR_BLOCK_H, "          █████▎    "),
            (-5.3, BAR_BLOCK_H, "    ▕█████          "),
            (+5.3, BAR_HEAVY_H, "          ━━━━━╸    "),
            (-5.3, BAR_HEAVY_H, "    ╺━━━━━          "),
            (+5.3, BAR_LIGHT_H, "          ─────╴    "),
            (-5.3, BAR_LIGHT_H, "    ╶─────          "),
            (+5.3, BAR_SHADE, "          █████░    "),
            (-5.3, BAR_SHADE, "    ░█████          "),
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
    def test_render(self, value: float, cells: Mark, expected: str):
        chart = Bar(
            value=value,
            value_range=(-10, 10),
            width=20,
            marks=cells,
        )
        assert render(chart) == expected


# class Test_StackedBar:
#     @pytest.mark.parametrize(
#         "values, bar_style, expected",
#         [
#             ([0.0, 5.2], BarStyle.BLOCK, " █████████▍         "),
#             ([5.2, 4.5], BarStyle.BLOCK, "██████████▍████████▍"),
#             ([5.2, 0.8], BarStyle.BLOCK, "██████████▍█        "),
#         ],
#         ids=["short+medium", "medium+medium", "medium+short"],
#     )
#     def test_render(self, values: List[float], bar_style: BarStyle, expected: str):
#         chart = StackedBar(
#             values=values,
#             value_range=(0, 10),
#             width=20,
#             end="",
#             colors=["purple", "blue"],
#         )
#         assert render(chart) == expected


# class Test_DoubleBar:
#     @pytest.mark.parametrize(
#         "values, bar_style, expected",
#         [
#             ([0.0, 5.2], BarStyle.BLOCK, "▄▄▄▄▄▄▄▄▄▄▄         "),
#             ([5.2, 9.5], BarStyle.BLOCK, "▀▀▀▀▀▀▀▀▀▀▀▄▄▄▄▄▄▄  "),
#             ([5.2, 6.8], BarStyle.BLOCK, "▀▀▀▀▀▀▀▀▀▀▀▄▄▄      "),
#             ([6.8, 5.2], BarStyle.BLOCK, "▀▀▀▀▀▀▀▀▀▀▀▀▀▀      "),
#         ],
#         ids=["short+medium", "medium+long", "medium+medium", "long+medium"],
#     )
#     def test_render(self, values: List[float], bar_style: BarStyle, expected: str):
#         chart = DoubleBar(
#             values=values,
#             value_range=(0, 10),
#             width=20,
#             end="",
#             colors=["purple", "blue"],
#         )
#         assert render(chart) == expected
