from typing import Optional

import pytest

from graphical.bar import Bar
from graphical.mark import BAR_BLOCK_H, BAR_HEAVY_H, BAR_LIGHT_H, BAR_SHADE, Mark
from graphical.utils import InversionStrategy
from tests.utilities.asserts import assert_markup


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
def test_positive(value: float, cells: Mark, expected: str):
    chart = Bar(
        value=value,
        value_range=(0, 10),
        length=20,
        marks=cells,
    )
    assert_markup(chart, expected)


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
def test_diverging(value: float, cells: Mark, expected: str):
    chart = Bar(
        value=value,
        value_range=(-10, 10),
        length=20,
        marks=cells,
    )
    assert_markup(chart, expected)


@pytest.mark.parametrize(
    "color,bgcolor,expected",
    [
        ("red", None, "[red]██████████▍[/red]         "),
        (None, "blue", "[on blue]██████████▍         [/on blue]"),
        (
            "red",
            "blue",
            "[red on blue]██████████▍[/red on blue][on blue]         [/on blue]",
        ),
    ],
    ids=[
        "color-only",
        "bgcolor-only",
        "color-and-bgcolor",
    ],
)
def test_positive_with_colors(color: str | None, bgcolor: str | None, expected: str):
    chart = Bar(
        value=5.2,
        value_range=(0, 10),
        length=20,
        color=color,
        bgcolor=bgcolor,
    )
    assert_markup(chart, expected)


@pytest.mark.parametrize(
    "marks, color,bgcolor, invert_negative, expected",
    [
        (
            BAR_BLOCK_H,
            "red",
            "blue",
            "swap",
            "[on blue]    [/on blue][blue on red]▊     [/blue on red][on blue]          [/on blue]",
        ),
        (
            BAR_BLOCK_H,
            "red",
            "blue",
            "reverse",
            "[on blue]    [/on blue][reverse red on blue]▕█████[/reverse red on blue][on blue]          [/on blue]",
        ),
        (
            BAR_HEAVY_H,
            "red",
            "blue",
            "swap",
            "[on blue]    [/on blue][red on blue]╺━━━━━[/red on blue][on blue]          [/on blue]",
        ),
        (
            BAR_HEAVY_H,
            "red",
            "blue",
            "reverse",
            "[on blue]    [/on blue][red on blue]╺━━━━━[/red on blue][on blue]          [/on blue]",
        ),
        (
            BAR_BLOCK_H,
            "red",
            None,
            "swap",
            "    [red]▕█████[/red]          ",
        ),
        (
            BAR_BLOCK_H,
            None,
            "blue",
            "swap",
            "[on blue]    ▕█████          [/on blue]",
        ),
    ],
    ids=[
        "swap-non-invertible-mark",
        "reverse-non-invertible-mark",
        "swap-without-bgcolor",
        "swap-without-color",
        "swap",
        "reverse",
    ],
)
def test_diverging_styled_inversion_markup(
    marks: Mark,
    color: str | None,
    bgcolor: str | None,
    invert_negative: Optional[InversionStrategy],
    expected: str,
):
    chart = Bar(
        value=-5.3,
        value_range=(-10, 10),
        length=20,
        marks=marks,
        color=color,
        bgcolor=bgcolor,
        invert_negative=invert_negative,
    )

    assert_markup(chart, expected, preview=True)
