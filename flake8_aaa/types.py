from enum import Enum

ActBlockType = Enum(  # pylint: disable=invalid-name
    'ActBlockType',
    'marked_act pytest_raises result_assignment unittest_raises',
)


class LineType(Enum):
    func_def = 'def'  # Function definition
    unprocessed = 'qqq'  # Not processed line

    def __str__(self) -> str:
        return '???' if self.value == 'qqq' else self.value
