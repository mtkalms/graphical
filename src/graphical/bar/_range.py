from typing import Optional, Tuple, Union

from rich.color import Color

from graphical.mark import Mark
from graphical.options import Orientation, InversionStrategy

from ._bar import Bar


class Range(Bar):
    """Bar with an offset.

    Args:
        data (Tuple[float, float]): Start and end point of range.
        value_range: Lower and upper boundary.
        length (int): The length of the graph. Defaults to 100.
        width (int): The width of the bars. Defaults to 1.
        marks (Union[BarMark, Mark]], optional): Marks used for the bar. Defaults to "block".
        color (Union[Color, str], optional): Color of the bar. Defaults to "default".
        bgcolor (Union[Color, str], optional): Background color. Defaults to "default".
        invert_negative (Literal["reverse",  "swap"], optional): Use positive marks and invert cell colors for negative number. If None or not supported by marks, the cell is not inverted.
        orientation: (Literal["horizontal", "vertical"], optional): The orientation of the bar. Defaults to "horizontal".
    """

    def __init__(
        self,
        data: Tuple[float, float],
        value_range: Tuple[float, float],
        *,
        length: Optional[int] = None,
        width: Optional[int] = None,
        marks: Optional[Mark] = None,
        color: Optional[Union[Color, str]] = None,
        bgcolor: Optional[Union[Color, str]] = None,
        invert_negative: Optional[InversionStrategy] = None,
        orientation: Orientation = "horizontal",
    ) -> None:
        super().__init__(
            max(data),
            value_range,
            length=length,
            width=width,
            marks=marks,
            color=color,
            bgcolor=bgcolor,
            invert_negative=invert_negative,
            orientation=orientation,
            origin=min(data),
            force_origin=False,
        )
