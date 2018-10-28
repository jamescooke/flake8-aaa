from enum import Enum

ActBlockType = Enum(  # pylint: disable=invalid-name
    'ActBlockType',
    'marked_act pytest_raises result_assignment unittest_raises',
)


class LineType(Enum):
    # Act
    act_block = 'act'
    # Function definition
    func_def = 'def'
    # Not processed line
    unprocessed = 'qqq'

    def __str__(self) -> str:
        return '???' if self.value == 'qqq' else self.value
