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
    """
    `with` statement is part of arrange. Blank lines are maintained around Act.
    """
    function.mark_bl()
    function.mark_def()
    function.mark_act()

    result = function.mark_arrange()

    assert result == 1
    assert function.line_markers == [
        LineType.func_def,
        LineType.arrange,
        LineType.blank_line,
        LineType.act,
        LineType.blank_line,
        LineType.unprocessed,
    ]
