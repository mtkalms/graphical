from graphical.section import Section


def _cell_value(bar: Section, segment: Section) -> float:
    intersection = segment.intersect(bar)
    # No intersection
    if not intersection:
        cell_value = 0.0
    # Full intersection
    elif segment == intersection:
        sign = -1.0 if bar.lower < 0 else 1.0
        cell_value = sign * 1.0
    # Partial intersection
    else:
        sign = 1.0 if intersection.middle < segment.middle else -1.0
        # Handle origin that falls between segment boundaries
        if segment.lower < 0.0 < segment.upper:
            cell_value = sign * -0.0 if bar in segment else sign * 0.5
        else:
            cell_value = sign * intersection.length / segment.length
    return cell_value
