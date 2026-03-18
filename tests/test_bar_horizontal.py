from typing import Optional

import pytest

from graphical.bar import Bar, InversionStrategy
from graphical.mark import Mark
from graphical.mark.horizontal import BAR_BLOCK_H, BAR_HEAVY_H, BAR_LIGHT_H
from graphical.mark.chromatic import BAR_SHADE
from tests.utilities.asserts import assert_markup


@pytest.mark.parametrize(
    "value, cells, expected",
    [
        (+0.0, BAR_BLOCK_H, "                    "),
        (+9.0, BAR_BLOCK_H, "          █████████ "),
        (-9.0, BAR_BLOCK_H, " █████████          "),
        (+8.0, BAR_BLOCK_H, "          ████████  "),
        (-8.0, BAR_BLOCK_H, "  ████████          "),
        (+6.7, BAR_BLOCK_H, "          ██████▊   "),
        (-6.7, BAR_BLOCK_H, "   ▐██████          "),
        (+5.6, BAR_BLOCK_H, "          █████▋    "),
        (-5.6, BAR_BLOCK_H, "    ▐█████          "),
        (+4.5, BAR_BLOCK_H, "          ████▌     "),
        (-4.5, BAR_BLOCK_H, "     ▐████          "),
        (+3.4, BAR_BLOCK_H, "          ███▍      "),
        (-3.4, BAR_BLOCK_H, "      ▐███          "),
        (+2.3, BAR_BLOCK_H, "          ██▎       "),
        (-2.3, BAR_BLOCK_H, "       ▕██          "),
        (+1.2, BAR_BLOCK_H, "          █▎        "),
        (-1.2, BAR_BLOCK_H, "        ▕█          "),
        (+0.1, BAR_BLOCK_H, "          ▏         "),
        (-0.1, BAR_BLOCK_H, "         ▕          "),
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
        "BLOCK_positive_partial_8",
        "BLOCK_negative_partial_8",
        "BLOCK_positive_partial_7",
        "BLOCK_negative_partial_7",
        "BLOCK_positive_partial_6",
        "BLOCK_negative_partial_6",
        "BLOCK_positive_partial_5",
        "BLOCK_negative_partial_5",
        "BLOCK_positive_partial_4",
        "BLOCK_negative_partial_4",
        "BLOCK_positive_partial_3",
        "BLOCK_negative_partial_3",
        "BLOCK_positive_partial_2",
        "BLOCK_negative_partial_2",
        "BLOCK_positive_partial_1",
        "BLOCK_negative_partial_1",
        "HEAVY_positive_partial",
        "HEAVY_negative_partial",
        "LIGHT_positive_partial",
        "LIGHT_negative_partial",
        "SHADE_positive_partial",
        "SHADE_negative_partial",
    ],
)
def test_marks(value: float, cells: Mark, expected: str):
    chart = Bar(
        data=value,
        value_range=(-10, 10),
        length=20,
        marks=cells,
    )
    assert_markup(chart, expected)


@pytest.mark.parametrize(
    "origin, force_origin, positive, negative",
    [
        (0.0, None, "         ▐█████████▏", "▕████████▌          "),
        (0.0, True, "         ▐█████████▏", "▕████████▌          "),
        (0.0, False, "         ▕█████████▏", "▕████████▉          "),
    ],
    ids=[
        "default",
        "force_origin",
        "leave_origin",
    ],
)
def test_origin(origin: float, force_origin: bool, positive: str, negative: str):
    chart = Bar(
        data=180,
        value_range=(-192, 196),
        length=20,
        marks=BAR_BLOCK_H,
        origin=origin,
        force_origin=force_origin,
    )
    assert_markup(chart, positive)

    chart = Bar(
        data=-180,
        value_range=(-192, 196),
        length=20,
        marks=BAR_BLOCK_H,
        origin=origin,
        force_origin=force_origin,
    )
    assert_markup(chart, negative)


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
def test_style(color: Optional[str], bgcolor: Optional[str], expected: str):
    chart = Bar(
        data=5.2,
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
        "swap",
        "reverse",
        "swap-non-invertible-mark",
        "reverse-non-invertible-mark",
        "swap-without-bgcolor",
        "swap-without-color",
    ],
)
def test_style_inversion(
    marks: Mark,
    color: Optional[str],
    bgcolor: Optional[str],
    invert_negative: Optional[InversionStrategy],
    expected: str,
):
    chart = Bar(
        data=-5.3,
        value_range=(-10, 10),
        length=20,
        marks=marks,
        color=color,
        bgcolor=bgcolor,
        invert_negative=invert_negative,
    )

    assert_markup(chart, expected)
