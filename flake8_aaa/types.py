from enum import Enum

ActBlockType = Enum(  # pylint: disable=invalid-name
    'ActBlockType',
    'marked_act pytest_raises result_assignment unittest_raises',
)


class LineType(Enum):
    # Act
    act_block = 'ACT'
    # Arrange
    arrange_block = 'ARR'
    # Function definition
    func_def = 'DEF'
    # Not processed line
    unprocessed = 'QQQ'

    def __str__(self) -> str:
        return '???' if self == self.unprocessed else self.value
