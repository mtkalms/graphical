from typing import Optional

import pytest

from graphical.bar import Stack
from graphical.mark import Mark
from graphical.mark.chromatic import BAR_SHADE
from graphical.mark.vertical import BAR_BLOCK_V, BAR_HEAVY_V, BAR_LIGHT_V
from graphical.utils import InversionStrategy
from tests.utilities.asserts import assert_markup


@pytest.mark.parametrize(
    "values, marks, expected",
    [
        (
            [0.0],
            BAR_BLOCK_V,
            (" \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n"),
        ),
        (
            [3.0, 2.6],
            BAR_BLOCK_V,
            (
                " \n \n \n \n \n \n \n \n"
                "[green]▂[/green]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[green on red]█[/green on red]\n"
                "[red on green]█[/red on green]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
            ),
        ),
        (
            [-3.0, -2.6],
            BAR_BLOCK_V,
            (
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[green on red] [/green on red]\n"
                "[red on green] [/red on green]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[green]▔[/green]\n"
                " \n \n \n \n \n \n \n \n"
            ),
        ),
        (
            [2.5, 2.8],
            BAR_HEAVY_V,
            (
                " \n \n \n \n \n \n \n \n \n"
                "[green]╻[/green]\n"
                "[green]┃[/green]\n"
                "[green]┃[/green]\n"
                "[green]┃[/green]\n"
                "[green]┃[/green]\n"
                "[green]┃[/green]\n"
                "[red]┃[/red]\n"
                "[red]┃[/red]\n"
                "[red]┃[/red]\n"
                "[red]┃[/red]\n"
                "[red]┃[/red]\n"
            ),
        ),
        (
            [-2.5, -2.8],
            BAR_LIGHT_V,
            (
                "[red]│[/red]\n"
                "[red]│[/red]\n"
                "[red]│[/red]\n"
                "[red]│[/red]\n"
                "[red]│[/red]\n"
                "[green]│[/green]\n"
                "[green]│[/green]\n"
                "[green]│[/green]\n"
                "[green]│[/green]\n"
                "[green]│[/green]\n"
                "[green]╵[/green]\n"
                " \n \n \n \n \n \n \n \n \n"
            ),
        ),
        (
            [2.5, 2.8],
            BAR_SHADE,
            (
                " \n \n \n \n \n \n \n \n \n"
                "[green]▒[/green]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[green on red]█[/green on red]\n"
                "[red on green]█[/red on green]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
            ),
        ),
    ],
    ids=[
        "BLOCK_none",
        "BLOCK_positive",
        "BLOCK_negative",
        "HEAVY_positive",
        "LIGHT_negative",
        "SHADE_positive",
    ],
)
def test_marks(values: list[float], marks: Mark, expected: str):
    chart = Stack(
        values=values,
        value_range=(-10, 10) if values == [0.0] else ((0, 10) if values[0] >= 0 else (-10, 0)),
        length=20,
        marks=marks,
        colors=["red", "green"],
        orientation="vertical",
    )
    assert_markup(chart, expected)


@pytest.mark.parametrize(
    "origin, force_origin, positive, negative",
    [
        (
            0.0,
            None,
            (
                "[green]▁[/green]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[red on green]▁[/red on green]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]▀[/red]\n"
                " \n \n \n \n \n \n \n \n \n"
            ),
            (
                " \n \n \n \n \n \n \n \n \n \n"
                "[red]▄[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[green on red]▆[/green on red]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[green]▔[/green]\n"
            ),
        ),
        (
            0.0,
            True,
            (
                "[green]▁[/green]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[red on green]▁[/red on green]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]▀[/red]\n"
                " \n \n \n \n \n \n \n \n \n"
            ),
            (
                " \n \n \n \n \n \n \n \n \n \n"
                "[red]▄[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[green on red]▆[/green on red]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[green]▔[/green]\n"
            ),
        ),
        (
            0.0,
            False,
            (
                "[green]▁[/green]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[red on green]▁[/red on green]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]▔[/red]\n"
                " \n \n \n \n \n \n \n \n \n"
            ),
            (
                " \n \n \n \n \n \n \n \n \n \n"
                "[red]▇[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[green on red]▆[/green on red]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[green]▔[/green]\n"
            ),
        ),
    ],
    ids=[
        "default",
        "force_origin",
        "leave_origin",
    ],
)
def test_origin(origin: float, force_origin: bool, positive: str, negative: str):
    chart = Stack(
        values=[120, 60],
        value_range=(-192, 196),
        length=20,
        marks=BAR_BLOCK_V,
        colors=["red", "green"],
        origin=origin,
        force_origin=force_origin,
        orientation="vertical",
    )
    assert_markup(chart, positive)

    chart = Stack(
        values=[-120, -60],
        value_range=(-192, 196),
        length=20,
        marks=BAR_BLOCK_V,
        colors=["red", "green"],
        origin=origin,
        force_origin=force_origin,
        orientation="vertical",
    )
    assert_markup(chart, negative)


@pytest.mark.parametrize(
    "colors,bgcolor,expected",
    [
        (
            ["magenta", "cyan"],
            None,
            (
                " \n \n \n \n \n \n \n \n \n"
                "[cyan]▃[/cyan]\n"
                "[cyan]█[/cyan]\n"
                "[cyan]█[/cyan]\n"
                "[cyan]█[/cyan]\n"
                "[cyan]█[/cyan]\n"
                "[magenta on cyan]▃[/magenta on cyan]\n"
                "[magenta]█[/magenta]\n"
                "[magenta]█[/magenta]\n"
                "[magenta]█[/magenta]\n"
                "[magenta]█[/magenta]\n"
                "[magenta]█[/magenta]\n"
            ),
        ),
        (
            ["magenta", "cyan"],
            "yellow",
            (
                "[on yellow] [/on yellow]\n"
                "[on yellow] [/on yellow]\n"
                "[on yellow] [/on yellow]\n"
                "[on yellow] [/on yellow]\n"
                "[on yellow] [/on yellow]\n"
                "[on yellow] [/on yellow]\n"
                "[on yellow] [/on yellow]\n"
                "[on yellow] [/on yellow]\n"
                "[on yellow] [/on yellow]\n"
                "[cyan on yellow]▃[/cyan on yellow]\n"
                "[cyan on yellow]█[/cyan on yellow]\n"
                "[cyan on yellow]█[/cyan on yellow]\n"
                "[cyan on yellow]█[/cyan on yellow]\n"
                "[cyan on yellow]█[/cyan on yellow]\n"
                "[magenta on cyan]▃[/magenta on cyan]\n"
                "[magenta on yellow]█[/magenta on yellow]\n"
                "[magenta on yellow]█[/magenta on yellow]\n"
                "[magenta on yellow]█[/magenta on yellow]\n"
                "[magenta on yellow]█[/magenta on yellow]\n"
                "[magenta on yellow]█[/magenta on yellow]\n"
            ),
        ),
    ],
    ids=[
        "custom-colors",
        "custom-colors-and-bgcolor",
    ],
)
def test_style(colors: list[str], bgcolor: Optional[str], expected: str):
    chart = Stack(
        values=[2.7, 2.5],
        value_range=(0, 10),
        length=20,
        colors=colors,
        bgcolor=bgcolor,
        orientation="vertical",
    )
    assert_markup(chart, expected)


@pytest.mark.parametrize(
    "marks, bgcolor, invert_negative, expected",
    [
        (
            BAR_BLOCK_V,
            "blue",
            "swap",
            (
                "[blue on red] [/blue on red]\n"
                "[blue on red] [/blue on red]\n"
                "[blue on red] [/blue on red]\n"
                "[blue on red] [/blue on red]\n"
                "[blue on red] [/blue on red]\n"
                "[green on red]▅[/green on red]\n"
                "[blue on green] [/blue on green]\n"
                "[blue on green] [/blue on green]\n"
                "[blue on green] [/blue on green]\n"
                "[blue on green] [/blue on green]\n"
                "[blue on green]▅[/blue on green]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
            ),
        ),
        (
            BAR_BLOCK_V,
            "blue",
            "reverse",
            (
                "[reverse red on blue]█[/reverse red on blue]\n"
                "[reverse red on blue]█[/reverse red on blue]\n"
                "[reverse red on blue]█[/reverse red on blue]\n"
                "[reverse red on blue]█[/reverse red on blue]\n"
                "[reverse red on blue]█[/reverse red on blue]\n"
                "[green on red]▅[/green on red]\n"
                "[reverse green on blue]█[/reverse green on blue]\n"
                "[reverse green on blue]█[/reverse green on blue]\n"
                "[reverse green on blue]█[/reverse green on blue]\n"
                "[reverse green on blue]█[/reverse green on blue]\n"
                "[reverse green on blue]▔[/reverse green on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
            ),
        ),
        (
            BAR_HEAVY_V,
            "blue",
            "swap",
            (
                "[red on blue]┃[/red on blue]\n"
                "[red on blue]┃[/red on blue]\n"
                "[red on blue]┃[/red on blue]\n"
                "[red on blue]┃[/red on blue]\n"
                "[red on blue]┃[/red on blue]\n"
                "[green on blue]┃[/green on blue]\n"
                "[green on blue]┃[/green on blue]\n"
                "[green on blue]┃[/green on blue]\n"
                "[green on blue]┃[/green on blue]\n"
                "[green on blue]┃[/green on blue]\n"
                "[green on blue]╹[/green on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
            ),
        ),
        (
            BAR_HEAVY_V,
            "blue",
            "reverse",
            (
                "[red on blue]┃[/red on blue]\n"
                "[red on blue]┃[/red on blue]\n"
                "[red on blue]┃[/red on blue]\n"
                "[red on blue]┃[/red on blue]\n"
                "[red on blue]┃[/red on blue]\n"
                "[green on blue]┃[/green on blue]\n"
                "[green on blue]┃[/green on blue]\n"
                "[green on blue]┃[/green on blue]\n"
                "[green on blue]┃[/green on blue]\n"
                "[green on blue]┃[/green on blue]\n"
                "[green on blue]╹[/green on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
                "[on blue] [/on blue]\n"
            ),
        ),
        (
            BAR_BLOCK_V,
            None,
            "swap",
            (
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[red]█[/red]\n"
                "[green on red]▅[/green on red]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[green]█[/green]\n"
                "[green]▔[/green]\n"
                " \n \n \n \n \n \n \n \n \n"
            ),
        ),
    ],
    ids=[
        "swap",
        "reverse",
        "swap-non-invertible-mark",
        "reverse-non-invertible-mark",
        "swap-without-bgcolor",
    ],
)
def test_style_inversion(
    marks: Mark,
    bgcolor: Optional[str],
    invert_negative: Optional[InversionStrategy],
    expected: str,
):
    chart = Stack(
        values=[-2.7, -2.5],
        value_range=(-10, 0),
        length=20,
        marks=marks,
        colors=["red", "green"],
        bgcolor=bgcolor,
        invert_negative=invert_negative,
        orientation="vertical",
    )

    assert_markup(chart, expected)
