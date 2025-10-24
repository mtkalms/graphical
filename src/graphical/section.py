from typing import Generator, Union


class Section(tuple):
    def __new__(cls, left: float, right: float) -> Section:
        return super().__new__(cls, (left, right))

    @property
    def left(self) -> float:
        return self[0]

    @property
    def right(self) -> float:
        return self[1]

    @property
    def middle(self) -> float:
        return (self.left + self.right) / 2.0

    @property
    def width(self) -> float:
        return abs(self.right - self.left)

    def __contains__(self, item: Union[float, Section]) -> bool:
        if isinstance(item, tuple):
            return self[0] <= item[0] and item[1] <= self[1]
        return self[0] <= item <= self[1]

    def segments(self, count: int) -> Generator[Section]:
        """Breaks this section into a given number of new sections of equal size.

        Args:
            count (int): Number of segments.

        Yields:
            Generator[Section]: Generator for segment sections.
        """
        step = self.width / count
        for n in range(count):
            yield Section(self.left + n * step, self.left + (n + 1) * step)

    def overlaps(self, other: Section) -> bool:
        """Returns if the given section has any overlap with this section.

        Args:
            other (Section): Other section.

        Returns:
            bool: Sections overlap.
        """
        return (
            other.left in self
            or other.right in self
            or self.left in other
            or self.right in other
        )

    def overlap(self, other: Section, normalize: bool = True) -> float:
        """Returns the signed width of the overlap between the given section and this one.
        The result is positive if the other section mainly overlaps the left half of this section, negative otherwise.
        If normalize is set to True, it will return the width of the overlap relative to the width of this section.

        Args:
            other (Section): Other section.
            normalize (bool, optional): Return width as fraction of this section. Defaults to True.

        Returns:
            float: Signed width of overlap
        """
        if not self.overlaps(other):
            return 0.0
        if self in other:
            return 1.0
        overlap = Section(max((self.left, other.left)), min((self.right, other.right)))
        left_overlap = max(
            (0.0, min((self.middle, overlap.right)) - max((self.left, overlap.left)))
        )
        right_overlap = max(
            (0.0, min((self.right, overlap.right)) - max((self.middle, overlap.left)))
        )
        sign = 1.0 if left_overlap >= right_overlap else -1.0
        return sign * overlap.width / self.width if normalize else sign * overlap.width
