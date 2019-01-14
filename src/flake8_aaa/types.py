from enum import Enum, unique

# TODO Adjust to Act Node types, not Act Block
ActBlockType = Enum(  # pylint: disable=invalid-name
    'ActBlockType',
    (
        'marked_act '   # Marked with "# act"
        'pytest_raises '  # Wrapped in "pytest.raises" context manager.
        'result_assignment '  # Simple "result = "
        'unittest_raises '  # Wrapped in unittest's "assertRaises" context manager.
    ),
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
