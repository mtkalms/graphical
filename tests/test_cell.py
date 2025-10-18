from typing import List

import pytest

from graphical.cell import PlotCellStyle, PlotCellRenderer


class Test_PlotCellRenderer:
    @pytest.mark.parametrize(
        "cell_style, num_values, expected_values",
        [(s, len(s.chars), s.chars) for s in PlotCellStyle],
        ids=[s.name for s in PlotCellStyle],
    )
    def test_render_range(
        self, cell_style: PlotCellStyle, num_values: int, expected_values: List[str]
    ):
        value_range = (0, num_values - 1)
        for value in range(num_values):
            expected = expected_values[value]
            result = PlotCellRenderer.render(
                value=value, value_range=value_range, cell_style=cell_style
            )
            message = f"Value {value} in range {value_range} is rendered for {cell_style.name} as {result}, not {expected}."
            assert result == expected, message

    @pytest.mark.parametrize(
        "cell_style, expected",
        [(s, s.over) for s in PlotCellStyle],
        ids=[s.name for s in PlotCellStyle],
    )
    def test_render_over(self, cell_style: PlotCellStyle, expected: str):
        value = 8
        value_range = (1, 7)
        result = PlotCellRenderer.render(
            value=value, value_range=value_range, cell_style=cell_style
        )
        message = f"Out of range (over) value is rendered for {cell_style.name} as {result}, not {expected}."
        assert result == expected, message

    @pytest.mark.parametrize(
        "cell_style, expected",
        [(s, s.under) for s in PlotCellStyle],
        ids=[s.name for s in PlotCellStyle],
    )
    def test_render_under(self, cell_style: PlotCellStyle, expected: str):
        value = 0
        value_range = (1, 7)
        result = PlotCellRenderer.render(
            value=value, value_range=value_range, cell_style=cell_style
        )
        message = f"Out of range (under) value is rendered for {cell_style.name} as {result}, not {expected}."
        assert result == expected, message
