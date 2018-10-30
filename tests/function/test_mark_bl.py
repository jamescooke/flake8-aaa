import pytest

from flake8_aaa.types import LineType


@pytest.mark.parametrize(
    'code_str', [
        '''
def test():
    """
    Do some testing.

    Note:
        This does not pass AAA :D
    """
    nums = (
        1,

        2,
    )

    result = len(nums)

    assert result == 2
'''
    ]
)
def test(function):
    function.line_markers[0] == LineType.func_def

    result = function.mark_bl()

    assert result == 2
    assert function.line_markers == 12 * [
        LineType.unprocessed,
    ] + [
        LineType.blank_line,
        LineType.unprocessed,  # result = ...
        LineType.blank_line,
        LineType.unprocessed,  # assert ...
    ]
