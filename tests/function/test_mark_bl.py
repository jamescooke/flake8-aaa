import pytest

from flake8_aaa.types import LineType


@pytest.mark.parametrize(
    'code_str', [
        '''
@pytest.mark.parametrize('messages', [

    """hi

    the end""",

])
def test(
    messages,
    x,

    y,
):
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
    result = function.mark_bl()

    assert result == 6
    assert function.line_markers.types == [
        LineType.unprocessed,  # @pytest.mark.parametrize('messages', [
        LineType.blank_line,
        LineType.unprocessed,  # """hi
        LineType.unprocessed,  # <<< This is a blank line in a string
        LineType.unprocessed,  # the end""",
        LineType.blank_line,
        LineType.unprocessed,  # ])
        LineType.unprocessed,  # def test(
        LineType.unprocessed,  # messages,
        LineType.unprocessed,  # x,
        LineType.blank_line,
        LineType.unprocessed,  # y,
        LineType.unprocessed,  # ):
        LineType.unprocessed,  # """
        LineType.unprocessed,  # Do some testing.
        LineType.unprocessed,
        LineType.unprocessed,  # Note:
        LineType.unprocessed,  # This does not pass AAA :D
        LineType.unprocessed,  # """
        LineType.unprocessed,  # nums = (
        LineType.unprocessed,  # 1,
        LineType.blank_line,
        LineType.unprocessed,  # 2,
        LineType.unprocessed,  # )
        LineType.blank_line,
        LineType.unprocessed,  # result = ...
        LineType.blank_line,
        LineType.unprocessed,  # assert ...
    ]


@pytest.mark.parametrize(
    'code_str', ['''
def test():
    x = 1
    y = 1


    result = x + y

    assert result == 2
''']
)
def test_double_space(function):
    result = function.mark_bl()

    assert function.line_markers.types == [
        LineType.unprocessed,  # def test()
        LineType.unprocessed,  # x = 1
        LineType.unprocessed,  # y = 1
        LineType.blank_line,  # ===  line no = 5
        LineType.blank_line,  # ===  line no = 6
        LineType.unprocessed,  # result = ...
        LineType.blank_line,  # ===  line no = 8
        LineType.unprocessed,  # assert ...
    ]
    assert result == 3
