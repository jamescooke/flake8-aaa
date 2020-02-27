import typing

from .exceptions import AAAError, ValidationError
from .helpers import first_non_blank_char
from .types import LineType


class LineMarkers(list):
    """
    Marks each line of a test function with the ``LineType`` assigned to that
    line.
    """

    def __init__(self, lines: typing.List[str], fn_offset: int) -> None:
        super().__init__([LineType.unprocessed] * len(lines))
        self.lines = lines  # type: typing.List[str]
        self.fn_offset = fn_offset  # type: int

    @typing.overload  # noqa: F811
    def __setitem__(self, key: int, value: typing.Any) -> None:
        pass

    @typing.overload  # noqa: F811
    def __setitem__(self, s: slice, o: typing.Iterable) -> None:
        pass

    def __setitem__(self, key, value):  # noqa: F811
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

        if not blank_lines or len(blank_lines) != 1:
            # Point at first line of second block
            yield self.build_error(
                line_index=second_block_lineno,
                text=error_message.format('none' if not blank_lines else len(blank_lines)),
            )
            return

    def check_blank_lines(self) -> typing.Generator[AAAError, None, None]:
        checked_blocks = (LineType.func_def, LineType.arrange, LineType.act, LineType._assert)
        for num, line_type in list(enumerate(self)):
            if (
                line_type is LineType.blank_line and self[num - 1] in checked_blocks and self[num - 1] == self[num + 1]
            ):
                yield self.build_error(
                    line_index=num,
                    text='AAA05 blank line in block',
                )

    def build_error(self, line_index: int, text: str) -> AAAError:
        """
        Calculate the offset of the error based on the first non-blank
        character of the line.
        """
        return AAAError(
            line_number=self.fn_offset + line_index,
            offset=first_non_blank_char(self.lines[line_index]),
            text=text,
        )
