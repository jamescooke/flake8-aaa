import pytest

from flake8_aaa.types import LineType


@pytest.mark.parametrize('code_str', [
    '''
def test():
    x = 1

    result = x ^ x

    assert result == 1
''',
])
def test(function):
    result = function.mark_line_types()

    assert result is None
    print(function.line_markers.data)
    assert function.line_markers.data == [
        LineType.func_def,
        LineType.unprocessed,
        LineType.blank_line,
        LineType.unprocessed,
        LineType.blank_line,
        LineType.unprocessed,
    ]
