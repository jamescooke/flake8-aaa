from typing import List

from .exceptions import ValidationError
from .types import LineType


class LineMarkers:
    """
    Marks each line of a test function with the ``LineType`` assigned to that
    line.

    Attributes:
        data: List of assigned ``LineTypes``.
        first_line_no: Line number of test function in test file.
    """

    def __init__(self, first_line_no: int, size: int) -> None:
        self.first_line_no = first_line_no  # type: int
        self.data = [LineType.unprocessed] * size  # type: List[LineType]

    def update(self, footprint: List[int], line_type: LineType) -> None:
        """
        Updates line types for a block's footprint.

        Raises:
            ValidationError: A special error on collision. This prevents Flake8
                from crashing because it is converted to a Flake8 error tuple,
                but it indicates to the user that something went wrong with
                processing the function.
        """
        for i in footprint:
            index = i - self.first_line_no
            if self.data[index] is not LineType.unprocessed:
                raise ValidationError(
                    i,
                    1,
                    'AAA99 Collision when marking this line as {}, was already {}'.format(
                        line_type,
                        self.data[index],
                    ),
                )
            self.data[index] = line_type
