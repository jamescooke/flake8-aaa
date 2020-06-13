from enum import Enum, unique

ActNodeType = Enum(
    'ActNodeType',
    (
        'marked_act '  # Marked with "# act"
        'pytest_raises '  # Wrapped in "pytest.raises" context manager.
        'result_assignment '  # Simple "result = "
        'unittest_raises '  # Wrapped in unittest's "assertRaises" context manager.
    ),
)


@unique
class LineType(Enum):
    # Act
    act = 'ACT'
    # Arrange
    arrange = 'ARR'
    # Assert
    _assert = 'ASS'
    # Blank line
    blank_line = 'BL '
    # Function definition
    func_def = 'DEF'
    # Comments
    comment = 'CMT'
    # Not processed line
    unprocessed = 'QQQ'

    def __str__(self) -> str:
        return '???' if self == self.unprocessed else self.value
