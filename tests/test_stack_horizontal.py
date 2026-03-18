from typing import Optional

import pytest

from graphical.bar import Stack, InversionStrategy
from graphical.mark import Mark
from graphical.mark.chromatic import BAR_SHADE
from graphical.mark.horizontal import BAR_BLOCK_H, BAR_HEAVY_H, BAR_LIGHT_H
from tests.utilities.asserts import assert_markup


@pytest.mark.parametrize(
    "values, marks, expected",
    [
        ([0.0], BAR_BLOCK_H, "                    "),
        (
            [3.0, 2.6],
            BAR_BLOCK_H,
            "[red]█████[/red][red on green]█ [/red on green][green]████▎[/green]        ",
        ),
        (
            [-3.0, -2.6],
            BAR_BLOCK_H,
            "        [green]▕████[/green][green on red]█ [/green on red][red]█████[/red]",
        ),
        (
            [2.5, 2.8],
            BAR_HEAVY_H,
            "[red]━━━━━[/red][green]━━━━━╸[/green]         ",
        ),
        (
            [-2.5, -2.8],
            BAR_LIGHT_H,
            "         [green]╶─────[/green][red]─────[/red]",
        ),
        (
            [2.5, 2.8],
            BAR_SHADE,
            "[red]████[/red][red on green]█ [/red on green][green]████▒[/green]         ",
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
    )
    assert_markup(chart, expected)


@pytest.mark.parametrize(
    "origin, force_origin, positive, negative",
    [
        (
            0.0,
            None,
            "         [red]▐██████[/red][red on green]▏[/red on green][green]██▏[/green]",
            "[green]▕██[/green][green on red]▊[/green on red][red]█████▌[/red]          ",
        ),
        (
            0.0,
            True,
            "         [red]▐██████[/red][red on green]▏[/red on green][green]██▏[/green]",
            "[green]▕██[/green][green on red]▊[/green on red][red]█████▌[/red]          ",
        ),
        (
            0.0,
            False,
            "         [red]▕██████[/red][red on green]▏[/red on green][green]██▏[/green]",
            "[green]▕██[/green][green on red]▊[/green on red][red]█████▉[/red]          ",
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
        marks=BAR_BLOCK_H,
        colors=["red", "green"],
        origin=origin,
        force_origin=force_origin,
    )
    assert_markup(chart, positive)

    chart = Stack(
        values=[-120, -60],
        value_range=(-192, 196),
        length=20,
        marks=BAR_BLOCK_H,
        colors=["red", "green"],
        origin=origin,
        force_origin=force_origin,
    )
    assert_markup(chart, negative)


@pytest.mark.parametrize(
    "colors,bgcolor,expected",
    [
        (
            ["magenta", "cyan"],
            None,
            "[magenta]█████[/magenta][magenta on cyan]▍[/magenta on cyan][cyan]████▍[/cyan]         ",
        ),
        (
            ["magenta", "cyan"],
            "yellow",
            "[magenta on yellow]█████[/magenta on yellow][magenta on cyan]▍[/magenta on cyan][cyan on yellow]████▍[/cyan on yellow][on yellow]         [/on yellow]",
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
    )
    assert_markup(chart, expected)


@pytest.mark.parametrize(
    "marks, bgcolor, invert_negative, expected",
    [
        (
            BAR_BLOCK_H,
            "blue",
            "swap",
            "[on blue]         [/on blue][blue on green]▋    [/blue on green][green on red]▋[/green on red][blue on red]     [/blue on red]",
        ),
        (
            BAR_BLOCK_H,
            "blue",
            "reverse",
            "[on blue]         [/on blue][reverse green on blue]▐████[/reverse green on blue][green on red]▋[/green on red][reverse red on blue]█████[/reverse red on blue]",
        ),
        (
            BAR_HEAVY_H,
            "blue",
            "swap",
            "[on blue]         [/on blue][green on blue]╺━━━━━[/green on blue][red on blue]━━━━━[/red on blue]",
        ),
        (
            BAR_HEAVY_H,
            "blue",
            "reverse",
            "[on blue]         [/on blue][green on blue]╺━━━━━[/green on blue][red on blue]━━━━━[/red on blue]",
        ),
        (
            BAR_BLOCK_H,
            None,
            "swap",
            "         [green]▐████[/green][green on red]▋[/green on red][red]█████[/red]",
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
    )

    assert_markup(chart, expected)
