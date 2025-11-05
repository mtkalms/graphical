from __future__ import annotations
from typing import Any, Generator, Union


class Section(tuple):
    """Represents a one dimensional section along an axis,
       defined by its lower and upper boundary positions.

    Args:
        tuple (_type_): Boundary positions.
    """

    def __new__(cls, lower: float, upper: float) -> Section:
        if lower > upper:
            print(lower, upper)
            raise ValueError("Upper boundary must be higher that lower boundary.")
        return super().__new__(cls, (lower, upper))

    @property
    def lower(self) -> float:
        """Get position of lower boundary.

        Returns:
            float: Position of lower boundary.
        """
        return self[0]

    @property
    def upper(self) -> float:
        """Get position of upper boundary.

        Returns:
            float: Position of upper boundary.
        """
        return self[1]

    @property
    def middle(self) -> float:
        """Get middle position of section.

        Returns:
            float: Middle position.
        """
        return (self.lower + self.upper) / 2.0

    @property
    def length(self) -> float:
        """Get length of section.

        Returns:
            float: Length of section.
        """
        return abs(self.upper - self.lower)

    def __contains__(self, other: Any) -> bool:
        if isinstance(other, tuple):
            return self.lower <= other[0] and other[1] <= self.upper
        if isinstance(other, (int, float)):
            return self.lower <= other <= self.upper
        raise ValueError()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, tuple):
            return self.lower == other[0] and self.upper == other[1]
        raise ValueError()

    def segment(self, count: int) -> Generator[Section]:
        """Segments the section into a given number of new sections of equal size.

        Args:
            count (int): Number of segments.

        Yields:
            Generator[Section]: Generator for resulting sections.
        """
        step = self.length / count
        for n in range(count):
            yield Section(self.lower + n * step, self.lower + (n + 1) * step)

    def overlaps(self, other: Section) -> bool:
        """Returns if this section has any overlap with another.

        Args:
            other (Section): Other section.

        Returns:
            bool: Sections overlap.
        """
        return (self.lower <= other[1]) and (self.upper >= other[0])

    def merge(self, other: Section) -> Section | None:
        """Merges this section with another one and returns the resulting section.

        Args:
            other (Section): Other section.

        Returns:
            Section | None: Merged section.
        """
        if not self.overlaps(other):
            return None
        return Section(min((self.lower, other.lower)), max((self.upper, other.upper)))

    def intersect(self, other: Section) -> Section | None:
        """Returns the intersection of this and another section.

        Args:
            other (Section): Other section.

        Returns:
            Section | None: Intersection with given section.
        """
        if not self.overlaps(other):
            return None
        return Section(max((self.lower, other.lower)), min((self.upper, other.upper)))
