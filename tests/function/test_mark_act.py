import pytest

from flake8_aaa.types import LineType


@pytest.mark.parametrize(
    'code_str', [
        '''
def test(hello_world_path):
    with open(hello_world_path) as f:

        result = f.read()

    assert result == 'Hello World!'
'''
    ]
)
def test_simple(function):
    function.mark_bl()
    function.mark_def()

    result = function.mark_act()

    assert result == 1
    assert function.line_markers == [
        LineType.func_def,
        LineType.unprocessed,
        LineType.blank_line,
        LineType.act,
        LineType.blank_line,
        LineType.unprocessed,
    ]
