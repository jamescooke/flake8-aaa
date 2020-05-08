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
    assert function_marked_bl_def_act_arr.line_markers.types == [
        LineType.func_def,
        LineType.arrange,
        LineType.blank_line,
        LineType.act,
        LineType.blank_line,
        LineType._assert,
    ]


# NOTE temporary tests to keep arrange blocks built the same with comments
# until #148 is done


@pytest.mark.parametrize(
    'code_str', [
        '''
def test_comment_after_act():
    x = 1
    y = 2

    result = x + y
    # Sum x and y

    assert result == 2
'''
    ]
)
def test_comment_after_act(function_marked_bl_def_act_arr):
    """
    Act block with trailing comment, comment is not marked as Assert
    """
    result = function_marked_bl_def_act_arr.mark_assert()

    assert result == 1
    assert function_marked_bl_def_act_arr.line_markers.types == [
        LineType.func_def,
        LineType.arrange,
        LineType.arrange,
        LineType.blank_line,
        LineType.act,
        LineType.unprocessed,
        LineType.blank_line,
        LineType._assert,
    ]


@pytest.mark.parametrize(
    'code_str', [
        '''
def test_comment_before_assert():
    x = 1
    y = 2

    result = x + y

    # Always 2
    assert result == 2
'''
    ]
)
def test_comment_start_assert(function_marked_bl_def_act_arr):
    """
    Comment at start of Assert remains unprocessed
    """
    result = function_marked_bl_def_act_arr.mark_assert()

    assert result == 1
    assert function_marked_bl_def_act_arr.line_markers.types == [
        LineType.func_def,
        LineType.arrange,
        LineType.arrange,
        LineType.blank_line,
        LineType.act,
        LineType.blank_line,
        LineType.unprocessed,
        LineType._assert,
    ]
