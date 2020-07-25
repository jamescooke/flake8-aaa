import pytest

from flake8_aaa.types import LineType


@pytest.mark.parametrize('code_str', ['''
def test():
    # Excellent test
    result = 1

    assert result == 1
'''])
def test(function_bl):
    result = function_bl.mark_comments()

    assert result == 1
    assert function_bl.line_markers.types == [
        LineType.unprocessed,
        LineType.comment,
        LineType.unprocessed,
        LineType.blank_line,
        LineType.unprocessed,
    ]


@pytest.mark.parametrize(
    'code_str', [
        '''
def test():
    message = """
# Not a comment - it's a string
"""

    result = len(message)  # noqa

    assert result == 33
    '''
    ]
)
def test_comments_in_strings(function_bl):
    result = function_bl.mark_comments()

    assert result == 0
    assert function_bl.line_markers.types == [
        LineType.unprocessed,
        LineType.unprocessed,
        LineType.unprocessed,
        LineType.unprocessed,
        LineType.blank_line,
        LineType.unprocessed,
        LineType.blank_line,
        LineType.unprocessed,
    ]
