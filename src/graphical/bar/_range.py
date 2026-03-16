from typing import Optional, Tuple, Union

from rich.color import Color

from ._bar import Bar
from ._types import Orientation, Numeric
from graphical.mark import Mark
from graphical.utils import InversionStrategy


class Range(Bar):
    """Range bar.

    Args:
        data (Tuple[Numeric, Numeric]): Start and end point of range.
        value_range: Lower and upper boundary.
        length (int): The length of the graph. Defaults to 100.
        marks (Union[BarMark, Mark]], optional): Marks used for the bar. Defaults to "block".
        color (Union[Color, str], optional): Color of the bar. Defaults to "default".
        bgcolor (Union[Color, str], optional): Background color. Defaults to "default".
        invert_negative (Literal["reverse",  "swap"], optional): Use positive marks and invert cell colors for negative number. If None or not supported by marks, the cell is not inverted.
        orientation: (Literal["horizontal", "vertical"], optional): The orientation of the bar. Defaults to "horizontal".
    """

    def __init__(
        self,
        values: Tuple[Numeric, Numeric],
        value_range: Tuple[Numeric, Numeric],
        *,
        length: Optional[int] = None,
        marks: Optional[Mark] = None,
        color: Optional[Union[Color, str]] = None,
        bgcolor: Optional[Union[Color, str]] = None,
        invert_negative: Optional[InversionStrategy] = None,
        orientation: Orientation = "horizontal",
    ) -> None:
        super().__init__(
            max(values),
            value_range,
            length=length,
            marks=marks,
            color=color,
            bgcolor=bgcolor,
            invert_negative=invert_negative,
            orientation=orientation,
            origin=min(values),
            force_origin=False,
        )
