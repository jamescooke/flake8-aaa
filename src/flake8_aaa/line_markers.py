import typing

from .exceptions import AAAError, ValidationError
from .types import LineType


class LineMarkers(list):
    """
    Marks each line of a test function with the ``LineType`` assigned to that
    line.
    """

    def __init__(self, size: int, fn_offset: int) -> None:
        super().__init__([LineType.unprocessed] * size)
        self.fn_offset = fn_offset  # type: int

    @typing.overload  # noqa: F811
    def __setitem__(self, key: int, value: typing.Any) -> None:
        pass

    @typing.overload  # noqa: F811
    def __setitem__(self, s: slice, o: typing.Iterable) -> None:  # pylint: disable=function-redefined
        pass

    def __setitem__(self, key, value):  # noqa: F811 | pylint: disable=function-redefined
        """
        Extended version of setitem to assert that item being replaced is
        always an unprocessed line. If the item being replaced is blank line,
        then do nothing.

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
        if current_type is LineType.blank_line:
            return
        if current_type is not LineType.unprocessed:
            raise ValueError('collision when marking this line as {}, was already {}'.format(
                value,
                current_type,
            ))
        return super().__setitem__(key, value)

    def update(self, span: typing.Tuple[int, int], line_type: LineType) -> None:
        """
        Updates line types for a block's span.

        Args:
            span: First and last relative line number of a Block.
            line_type: The type of line to update to.

        Raises:
            ValidationError: A special error on collision. This prevents Flake8
                from crashing because it is converted to a Flake8 error tuple,
                but it indicates to the user that something went wrong with
                processing the function.
        """
        first_block_line, last_block_line = span
        for i in range(first_block_line, last_block_line + 1):
            try:
                self.__setitem__(i, line_type)
            except ValueError as error:
                raise ValidationError(i + self.fn_offset, 1, 'AAA99 {}'.format(error))

    def check_arrange_act_spacing(self) -> typing.Generator[AAAError, None, None]:
        """
        * When no spaces found, point error at line above act block
        * When too many spaces found, point error at 2nd blank line
        """
        yield from self.check_block_spacing(
            LineType.arrange,
            LineType.act,
            'AAA03 expected 1 blank line before Act block, found {}',
        )

    def check_act_assert_spacing(self) -> typing.Generator[AAAError, None, None]:
        """
        * When no spaces found, point error at line above assert block
        * When too many spaces found, point error at 2nd blank line
        """
        yield from self.check_block_spacing(
            LineType.act,
            LineType._assert,
            'AAA04 expected 1 blank line before Assert block, found {}',
        )

    def check_block_spacing(
        self,
        first_block_type: LineType,
        second_block_type: LineType,
        error_message: str,
    ) -> typing.Generator[AAAError, None, None]:
        """
        Checks there is a clear single line between ``first_block_type`` and
        ``second_block_type``.

        Note:
            Is tested via ``check_arrange_act_spacing()`` and
            ``check_act_assert_spacing()``.
        """
        numbered_lines = list(enumerate(self))
        first_block_lines = filter(lambda l: l[1] is first_block_type, numbered_lines)
        try:
            first_block_lineno = list(first_block_lines)[-1][0]
        except IndexError:
            # First block has no lines
            return

        second_block_lines = filter(lambda l: l[1] is second_block_type, numbered_lines)
        try:
            second_block_lineno = next(second_block_lines)[0]
        except StopIteration:
            # Second block has no lines
            return

        blank_lines = [
            bl for bl in numbered_lines[first_block_lineno + 1:second_block_lineno] if bl[1] is LineType.blank_line
        ]

        if not blank_lines:
            # Point at line above second block
            yield AAAError(
                line_number=self.fn_offset + second_block_lineno - 1,
                offset=0,
                text=error_message.format('none'),
            )
            return

        if len(blank_lines) > 1:
            # Too many blank lines - point at the first extra one, the 2nd
            yield AAAError(
                line_number=self.fn_offset + blank_lines[1][0],
                offset=0,
                text=error_message.format(len(blank_lines)),
            )

    def check_blank_lines(self) -> typing.Generator[AAAError, None, None]:
        checked_blocks = (LineType.func_def, LineType.arrange, LineType.act, LineType._assert)
        for num, line_type in list(enumerate(self)):
            if (
                line_type is LineType.blank_line and self[num - 1] in checked_blocks and self[num - 1] == self[num + 1]
            ):
                yield AAAError(
                    line_number=self.fn_offset + num,
                    offset=0,
                    text='AAA05 blank line in block',
                )
