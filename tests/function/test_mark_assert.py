import pytest

from flake8_aaa.function import Function
from flake8_aaa.types import LineType


@pytest.fixture
def function_marked_bl_def_act_arr(function) -> Function:
    function.mark_bl()
    function.mark_def()
    function.mark_act()
    function.mark_arrange()
    return function


# --- TESTS ---


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
def test_simple(function_marked_bl_def_act_arr):
    """
    Assert is found on last line of test
    """
    result = function_marked_bl_def_act_arr.mark_assert()

    assert result == 1
    assert function_marked_bl_def_act_arr.line_markers == [
        LineType.func_def,
        LineType.arrange,
        LineType.blank_line,
        LineType.act,
        LineType.blank_line,
        LineType._assert,
    ]
