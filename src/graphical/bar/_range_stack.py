from typing import Optional, Sequence, Tuple, Union

from rich.color import Color

from graphical.mark import Mark
from graphical.options import Orientation, InversionStrategy

from ._stack import Stack


class RangeStack(Stack):
    """Stack with an offset.

    Args:
        data (Sequence[float]): The values in order of stacking. The first value is the stack offset.
        value_range: Lower and upper boundary. Defaults to range of data.
        length (int): The length of the graph. Defaults to 100.
        width (int): The width of the bars. Defaults to 1.
        marks (Union[BarMark, Mark]], optional): Marks used for the bars. Defaults to "block".
        colors (Sequence[Union[Color, str]], optional): Colors of the bars.
        bgcolor (Union[Color, str], optional): Background color. Defaults to "default".
        invert_negative (Literal["reverse",  "swap"], optional): Use positive marks and invert cell colors for negative number. If None or not supported by marks, the cell is not inverted.
        orientation: (Literal["horizontal", "vertical"], optional): The orientation of the bar. Defaults to "horizontal".
    """

    def __init__(
        self,
        data: Sequence[float],
        value_range: Tuple[float, float],
        *,
        length: Optional[int] = None,
        width: Optional[int] = None,
        marks: Optional[Mark] = None,
        colors: Sequence[Union[Color, str]] = ["red", "green", "blue", "yellow"],
        bgcolor: Optional[Union[Color, str]] = None,
        invert_negative: Optional[InversionStrategy] = None,
        orientation: Orientation = "horizontal",
    ) -> None:
        super().__init__(
            data[1:],
            value_range,
            length=length,
            width=width,
            marks=marks,
            colors=colors,
            bgcolor=bgcolor,
            invert_negative=invert_negative,
            orientation=orientation,
            origin=data[0],
            force_origin=False,
        )
