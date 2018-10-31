from typing import Any, Iterable, Set, Union, overload

from .exceptions import ValidationError
from .types import LineType


class LineMarkers(list):
    """
    Marks each line of a test function with the ``LineType`` assigned to that
    line.
    """

    def __init__(self, size: int) -> None:
        super().__init__([LineType.unprocessed] * size)

    @overload  # noqa: F811
    def __setitem__(self, key: int, value: Any) -> None:
        pass

    @overload  # noqa: F811
    def __setitem__(self, s: slice, o: Iterable) -> None:  # pylint: disable=function-redefined
        pass

    def __setitem__(self, key, value):  # noqa: F811 | pylint: disable=function-redefined
        """
        Extended version of setitem to assert that item being replaced is
        always an unprocessed line.

        Raises:
            NotImplementedError: When a slice is passed for ``key``.
            ValueError: When item being replaced is not unprocessed, or passed
                ``value`` is not a LineType.
        """
        if isinstance(key, slice):
            raise NotImplementedError('LineMarkers disallow slicing')
        if not isinstance(value, LineType):
            raise ValueError('"{}" for line {} is not LineType'.format(value, key))
        current_type = self.__getitem__(key)
        if current_type is not LineType.unprocessed:
            raise ValueError('collision when marking this line as {}, was already {}'.format(
                value,
                current_type,
            ))
        return super().__setitem__(key, value)

    def update(self, footprint: Union[range, Set[int]], line_type: LineType, offset: int) -> None:
        """
        Updates line types for a block's footprint.

        Args:
            footprint: This is a range or set of 0 indexed positions in the
                function that will be updated.
            line_type: The type of line to update to.
            offset: Line number of the 0th line of the test function in the
                test file. This is used to revert any exceptions raised back to
                the line number of the test file.

        Raises:
            ValidationError: A special error on collision. This prevents Flake8
                from crashing because it is converted to a Flake8 error tuple,
                but it indicates to the user that something went wrong with
                processing the function.
        """
        for i in footprint:
            try:
                self.__setitem__(i, line_type)
            except ValueError as error:
                raise ValidationError(i + offset, 1, 'AAA99 {}'.format(error))
