import pytest
from graphical.bar import Bar
from graphical.mark import BAR_BLOCK_H, BAR_HEAVY_H, BAR_LIGHT_H, BAR_SHADE, Mark
from tests.utilities.asserts import assert_markup


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
            length=20,
            marks=cells,
        )
        assert_markup(chart, expected)


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
            length=20,
            marks=cells,
        )
        assert_markup(chart, expected)
