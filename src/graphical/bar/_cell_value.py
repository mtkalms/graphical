from graphical.section import Section


def _cell_value(bar: Section, cell: Section) -> float:
    """Calculates in percentage the directional overlap between a bar and a cell.
    It considers two case: the bar overlaps the cell from the left (positive number),
    and the bar overlaps the cell from the right (negative number).
    Cases where the bar is completely contained by the cell are mapped to the closest approximation.


    Args:
        bar (Section): Value range of the bar.
        cell (Section): Value range of the cell.

    Returns:
        float: Directional overlap in percentage [-1.0, 1.0]
    """
    intersection = cell.intersect(bar)
    # No intersection
    if not intersection:
        cell_value = 0.0
    # Full intersection
    elif cell == intersection:
        sign = -1.0 if bar.lower < 0 else 1.0
        cell_value = sign * 1.0
    # Partial intersection
    else:
        sign = 1.0 if intersection.middle < cell.middle else -1.0
        # Handle origin that falls between cell boundaries
        if cell.lower < 0.0 < cell.upper:
            cell_value = sign * -0.0 if bar in cell else sign * 0.5
        else:
            cell_value = sign * intersection.length / cell.length
    return cell_value
