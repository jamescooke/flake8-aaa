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
