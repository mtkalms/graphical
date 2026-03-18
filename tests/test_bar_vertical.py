import pytest

from graphical.bar import Bar
from graphical.mark import Mark
from graphical.mark.chromatic import BAR_SHADE
from graphical.mark.vertical import BAR_BLOCK_V, BAR_HEAVY_V, BAR_LIGHT_V
from tests.utilities.asserts import assert_markup


@pytest.mark.parametrize(
    "value, cells, expected",
    [
        (
            +0.0,
            BAR_BLOCK_V,
            (" \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n"),
        ),
        (
            +9.0,
            BAR_BLOCK_V,
            (" \n█\n█\n█\n█\n█\n█\n█\n█\n█\n \n \n \n \n \n \n \n \n \n \n"),
        ),
        (
            -9.0,
            BAR_BLOCK_V,
            (" \n \n \n \n \n \n \n \n \n \n█\n█\n█\n█\n█\n█\n█\n█\n█\n \n"),
        ),
        (
            +8.0,
            BAR_BLOCK_V,
            (" \n \n█\n█\n█\n█\n█\n█\n█\n█\n \n \n \n \n \n \n \n \n \n \n"),
        ),
        (
            -8.0,
            BAR_BLOCK_V,
            (" \n \n \n \n \n \n \n \n \n \n█\n█\n█\n█\n█\n█\n█\n█\n \n \n"),
        ),
        (
            +6.7,
            BAR_BLOCK_V,
            (" \n \n \n▆\n█\n█\n█\n█\n█\n█\n \n \n \n \n \n \n \n \n \n \n"),
        ),
        (
            -6.7,
            BAR_BLOCK_V,
            (" \n \n \n \n \n \n \n \n \n \n█\n█\n█\n█\n█\n█\n▀\n \n \n \n"),
        ),
        (
            +5.6,
            BAR_BLOCK_V,
            (" \n \n \n \n▅\n█\n█\n█\n█\n█\n \n \n \n \n \n \n \n \n \n \n"),
        ),
        (
            -5.6,
            BAR_BLOCK_V,
            (" \n \n \n \n \n \n \n \n \n \n█\n█\n█\n█\n█\n▀\n \n \n \n \n"),
        ),
        (
            +4.5,
            BAR_BLOCK_V,
            (" \n \n \n \n \n▄\n█\n█\n█\n█\n \n \n \n \n \n \n \n \n \n \n"),
        ),
        (
            -4.5,
            BAR_BLOCK_V,
            (" \n \n \n \n \n \n \n \n \n \n█\n█\n█\n█\n▀\n \n \n \n \n \n"),
        ),
        (
            +3.4,
            BAR_BLOCK_V,
            (" \n \n \n \n \n \n▃\n█\n█\n█\n \n \n \n \n \n \n \n \n \n \n"),
        ),
        (
            -3.4,
            BAR_BLOCK_V,
            (" \n \n \n \n \n \n \n \n \n \n█\n█\n█\n▔\n \n \n \n \n \n \n"),
        ),
        (
            +2.3,
            BAR_BLOCK_V,
            (" \n \n \n \n \n \n \n▂\n█\n█\n \n \n \n \n \n \n \n \n \n \n"),
        ),
        (
            -2.3,
            BAR_BLOCK_V,
            (" \n \n \n \n \n \n \n \n \n \n█\n█\n▔\n \n \n \n \n \n \n \n"),
        ),
        (
            +1.2,
            BAR_BLOCK_V,
            (" \n \n \n \n \n \n \n \n▂\n█\n \n \n \n \n \n \n \n \n \n \n"),
        ),
        (
            -1.2,
            BAR_BLOCK_V,
            (" \n \n \n \n \n \n \n \n \n \n█\n▔\n \n \n \n \n \n \n \n \n"),
        ),
        (
            +0.1,
            BAR_BLOCK_V,
            (" \n \n \n \n \n \n \n \n \n▁\n \n \n \n \n \n \n \n \n \n \n"),
        ),
        (
            -0.1,
            BAR_BLOCK_V,
            (" \n \n \n \n \n \n \n \n \n \n▔\n \n \n \n \n \n \n \n \n \n"),
        ),
        (
            +5.3,
            BAR_HEAVY_V,
            (" \n \n \n \n╻\n┃\n┃\n┃\n┃\n┃\n \n \n \n \n \n \n \n \n \n \n"),
        ),
        (
            -5.3,
            BAR_HEAVY_V,
            (" \n \n \n \n \n \n \n \n \n \n┃\n┃\n┃\n┃\n┃\n╹\n \n \n \n \n"),
        ),
        (
            +5.3,
            BAR_LIGHT_V,
            (" \n \n \n \n╷\n│\n│\n│\n│\n│\n \n \n \n \n \n \n \n \n \n \n"),
        ),
        (
            -5.3,
            BAR_LIGHT_V,
            (" \n \n \n \n \n \n \n \n \n \n│\n│\n│\n│\n│\n╵\n \n \n \n \n"),
        ),
        (
            +5.3,
            BAR_SHADE,
            (" \n \n \n \n░\n█\n█\n█\n█\n█\n \n \n \n \n \n \n \n \n \n \n"),
        ),
        (
            -5.3,
            BAR_SHADE,
            (" \n \n \n \n \n \n \n \n \n \n█\n█\n█\n█\n█\n░\n \n \n \n \n"),
        ),
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
        orientation="vertical",
    )
    assert_markup(chart, expected)


@pytest.mark.parametrize(
    "origin, force_origin, positive, negative",
    [
        (
            0.0,
            None,
            ("▁\n█\n█\n█\n█\n█\n█\n█\n█\n█\n▀\n \n \n \n \n \n \n \n \n \n"),
            (" \n \n \n \n \n \n \n \n \n \n▄\n█\n█\n█\n█\n█\n█\n█\n█\n▔\n"),
        ),
        (
            0.0,
            True,
            ("▁\n█\n█\n█\n█\n█\n█\n█\n█\n█\n▀\n \n \n \n \n \n \n \n \n \n"),
            (" \n \n \n \n \n \n \n \n \n \n▄\n█\n█\n█\n█\n█\n█\n█\n█\n▔\n"),
        ),
        (
            0.0,
            False,
            ("▁\n█\n█\n█\n█\n█\n█\n█\n█\n█\n▔\n \n \n \n \n \n \n \n \n \n"),
            (" \n \n \n \n \n \n \n \n \n \n▇\n█\n█\n█\n█\n█\n█\n█\n█\n▔\n"),
        ),
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
        marks=BAR_BLOCK_V,
        origin=origin,
        force_origin=force_origin,
        orientation="vertical",
    )
    assert_markup(chart, positive)

    chart = Bar(
        data=-180,
        value_range=(-192, 196),
        length=20,
        marks=BAR_BLOCK_V,
        origin=origin,
        force_origin=force_origin,
        orientation="vertical",
    )
    assert_markup(chart, negative)
