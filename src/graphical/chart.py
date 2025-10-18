from dataclasses import dataclass
from typing import List, Tuple, Optional, Union

from rich.box import Box, HEAVY
from rich.console import RenderResult, RenderableType
from rich.segment import Segment


@dataclass
class LabelChartRow:
    """Content row for labeled chart.

    Args:
        content (Union[RenderableType, Segment]): RenderableType representing the content.
        content_width (int): Width of the content.
        label (str): Label of the content line.
    """

    content: Union[RenderableType, Segment]
    """Union[RenderableType, Segment]: Content line rendered in the chart."""
    content_width: int
    """int: Width of the chart"""
    label: str = ""
    """str: Label of the content line."""


class LabelChartRenderer:
    """Renderer for labeled charts.

    Args:
        title (str): The title of the chart rendered at the top.
        ticks (Tuple[float, float], optional): Minimum and maximum value to display on the x-axis.
        box (Box): One of the constants in rich.box used to draw the edges.
    """

    def __init__(
        self,
        title: str,
        ticks: Optional[Tuple[float, float]] = None,
        box: Box = HEAVY,
    ):
        self.title = title
        self.ticks = ticks
        self.box = box
        self.rows: List[LabelChartRow] = []

    def add_row(
        self,
        content: Union[RenderableType, Segment],
        content_width: int,
        label: str = "",
    ) -> LabelChartRow:
        """Add row to chart.

        Args:
            content (Union[RenderableType, Segment]): RenderableType representing the content.
            content_width (int): Width of the content.
            label (str): Label of the content line.

        Returns:
            LabelChartRow: Row created and added to LabelChartRenderer.
        """
        row = LabelChartRow(content, content_width, label)
        self.rows.append(row)
        return row

    def render(self) -> RenderResult:
        """Render the labeled chart.

        Returns:
            RenderResult: Rendered chart.
        """
        width_labels = max(len(d.label) for d in self.rows) + 1
        width_content = max(d.content_width for d in self.rows)

        yield Segment(" " * width_labels)
        yield Segment(f"{self.title: ^{width_content + 2}}")
        yield Segment("\n")

        yield Segment(" " * width_labels)
        yield Segment(self.box.top_left)
        yield Segment(self.box.top * width_content)
        yield Segment(self.box.top_right)
        yield Segment("\n")

        for row in self.rows:
            yield Segment(f"{row.label: >{width_labels - 1}} ")
            yield Segment(self.box.row_right)
            yield Segment(row.content) if type(row.content) is str else row.content
            yield Segment(" " * (width_content - row.content_width))
            yield Segment(self.box.mid_right)
            yield Segment("\n")

        yield Segment(" " * width_labels)
        yield Segment(self.box.bottom_left)
        yield Segment(self.box.bottom * width_content)
        yield Segment(self.box.bottom_right)
        yield Segment("\n")

        if self.ticks:
            yield Segment(" " * (width_labels + 1))
            yield Segment(f"{self.ticks[0]: <{width_content // 2}}")
            yield Segment(f"{self.ticks[1]: >{width_content - width_content // 2}}")
            yield Segment("\n")
