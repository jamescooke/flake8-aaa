from enum import Enum, unique

ActBlockType = Enum(  # pylint: disable=invalid-name
    'ActBlockType',
    'marked_act pytest_raises result_assignment unittest_raises',
)


@unique
class LineType(Enum):
    # Act
    act_block = 'ACT'
    # Arrange
    arrange_block = 'ARR'
    # Assert
    assert_block = 'ASS'
    # Blank line
    blank_line = 'BL '
    # Function definition
    func_def = 'DEF'
    # Not processed line
    unprocessed = 'QQQ'

    def __str__(self) -> str:
        return '???' if self == self.unprocessed else self.value
