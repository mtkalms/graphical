from dataclasses import dataclass
from typing import List, Tuple, Optional

from rich.box import Box, HEAVY
from rich.console import Console, ConsoleOptions, RenderResult, RenderableType
from rich.measure import Measurement
from rich.segment import Segment


@dataclass
class LabelChartRow:
    content: RenderableType
    content_width: int
    label: str = ""


class LabelChartRenderer:
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
        self, content: RenderableType, content_width: int, label: str = ""
    ) -> LabelChartRow:
        row = LabelChartRow(content, content_width, label)
        self.rows.append(row)
        return row

    def render(self) -> RenderResult:
        width_labels = max(len(d.label) for d in self.rows) + 1
        width_content = max(d.content_width for d in self.rows)

        yield Segment(" " * width_labels)
        yield Segment(f"{self.title : ^{width_content + 2}}")
        yield Segment("\n")

        yield Segment(" " * width_labels)
        yield Segment(self.box.top_left)
        yield Segment(self.box.top * width_content)
        yield Segment(self.box.top_right)
        yield Segment("\n")

        for row in self.rows:
            yield Segment(f"{row.label : >{width_labels - 1}} ")
            yield Segment(self.box.row_right)
            yield row.content
            yield Segment(self.box.mid_right)
            yield Segment("\n")

        yield Segment(" " * width_labels)
        yield Segment(self.box.bottom_left)
        yield Segment(self.box.bottom * width_content)
        yield Segment(self.box.bottom_right)
        yield Segment("\n")

        if self.ticks:
            yield Segment(" " * (width_labels + 1))
            yield Segment(f"{self.ticks[0] : <{width_content // 2}}")
            yield Segment(f"{self.ticks[1] : >{width_content - width_content // 2}}")
            yield Segment("\n")
