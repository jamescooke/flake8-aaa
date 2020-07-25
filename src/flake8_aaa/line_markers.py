from typing import Generator, List, Optional

from .exceptions import AAAError, ValidationError
from .helpers import first_non_blank_char
from .types import LineType


class LineMarkers:
    """
    Marks each line of a test function with the ``LineType`` assigned to that
    line.

    Attributes:
        lines: Lines of code that make up test. Used to calculate offset in
            raised error.
        types: List of types for each line in test.
        fn_offset: First line number of test so that line type indices can be
            converted back to line numbers in exceptions.
    """

    def __init__(self, lines: List[str], fn_offset: int) -> None:
        self.types = [LineType.unprocessed] * len(lines)
        self.lines = lines
        self.fn_offset = fn_offset

    def set(self, index: int, value: LineType) -> bool:
        """
        Extended version of setitem to assert that rules for setting a line are
        met:
            * Existing line is unprocessed - line is set as new type.
            * Existing line is blank line or comment and new line is function
                defintion or an AAA block - line setting is ignored because
                comments and blank lines can appear in func defs and blocks.

        Returns:
            An unprocessed line was replaced with a new line type.

        Raises:
            ValidationError: AAA99 marking caused a collision.
            ValueError: passed ``value`` is unprocessed line or is not a
                LineType.
        """
        if not isinstance(value, LineType):
            raise ValueError(f'"{value}" for line index {index} is not LineType')
        if value is LineType.unprocessed:
            raise ValueError(f'Can not revert line index {index} to "{value}"')
        current_type = self.types[index]
        if current_type is LineType.blank_line or current_type is LineType.comment:
            return False
        if current_type is not LineType.unprocessed:
            line_num = index + self.fn_offset
            raise ValidationError(
                line_num,
                1,
                f'AAA99 collision when marking line {line_num} (index={index}) as {value}, was already {current_type}',
            )
        self.types[index] = value
        return True

    def update(self, a: int, b: int, line_type: LineType) -> int:
        """
        Updates line types from index ``a`` to index ``b`` inclusively. Indexes
        are relative.

        Args:
            a: First line index.
            b: Last line index.
            line_type: New type of line.

        Returns:
            Number of lines updated. This may not be equal to ``b - a + 1``
                because lines that are blank are skipped.

        Raises:
            ValidationError: A special error on collision. This prevents Flake8
                from crashing because it is converted to a Flake8 error tuple,
                but it indicates to the user that something went wrong with
                processing the function.
        """
        count = 0

        for i in range(a, b + 1):
            if self.set(i, line_type):
                count += 1

        return count

    def previous(self, num: int) -> Optional[LineType]:
        """
        Returns:
            Previous line's type, relative to `num`. Returns `None` if we're at
            the first line.
        """
        try:
            return self.types[num - 1]
        except IndexError:
            return None

    def next(self, num) -> Optional[LineType]:
        """
        Returns:
            Next line's type, relative to `num`. Returns `None` if we're at the
            last line.
        """
        try:
            return self.types[num + 1]
        except IndexError:
            return None

    def check_arrange_act_spacing(self) -> Generator[AAAError, None, None]:
        """
        * When no spaces found, point error at line above act block
        * When too many spaces found, point error at 2nd blank line
        """
        yield from self.check_block_spacing(
            LineType.arrange,
            LineType.act,
            'AAA03 expected 1 blank line before Act block, found {}',
        )

    def check_act_assert_spacing(self) -> Generator[AAAError, None, None]:
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
    ) -> Generator[AAAError, None, None]:
        """
        Checks there is a clear single line between ``first_block_type`` and
        ``second_block_type``.

        Note:
            Is tested via ``check_arrange_act_spacing()`` and
            ``check_act_assert_spacing()``.
        """
        numbered_lines = list(enumerate(self.types))
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

    def check_blank_lines(self) -> Generator[AAAError, None, None]:
        checked_blocks = (LineType.func_def, LineType.arrange, LineType.act, LineType._assert)
        for num, line_type in enumerate(self.types):
            if (
                line_type is LineType.blank_line and self.types[num - 1] in checked_blocks
                and self.types[num - 1] == self.types[num + 1]
            ):
                yield self.build_error(
                    line_index=num,
                    text='AAA05 blank line in block',
                )

    def check_comment_in_act(self) -> Generator[AAAError, None, None]:
        for num, line_type in enumerate(self.types):
            if line_type is LineType.comment:
                if self.previous(num) == LineType.act or self.next(num) == LineType.act:
                    yield self.build_error(
                        line_index=num,
                        text='AAA06 comment in Act block',
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
