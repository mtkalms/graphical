from graphical.section import Section


def overlap(
    bar: Section,
    cell: Section,
    *,
    origin: float = 0.0,
    force_origin: bool = False,
) -> float:
    """Calculates in percentage the directional overlap between a bar and a cell.
    It considers two case: the bar overlaps the cell from the left (positive number),
    and the bar overlaps the cell from the right (negative number).
    Cases where the bar is completely contained by the cell are mapped to the closest approximation.


    Args:
        bar (Section): Value range of the bar.
        cell (Section): Value range of the cell.
        origin (float, optional): Origin point. Defaults to 0.0.
        force_origin (bool, optional): Force origin to half cell grid. Defaults to False.

    Returns:
        float: Directional overlap in percentage [-1.0, 1.0]
    """
    intersection = cell.intersect(bar)
    # No intersection
    if not intersection:
        result = 0.0
    # Full intersection
    elif cell == intersection:
        sign = -1.0 if bar.lower < origin else 1.0
        result = sign * 1.0
    # Partial intersection
    else:
        sign = 1.0 if intersection.middle < cell.middle else -1.0
        # Handle origin that falls between cell boundaries
        if force_origin and cell.lower < origin < cell.upper:
            # Force origin to middle of cell
            result = sign * -0.0 if bar in cell else sign * 0.5
        else:
            result = sign * intersection.length / cell.length
    return result
