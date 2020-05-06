import pytest

from flake8_aaa.function import Function
from flake8_aaa.types import LineType


@pytest.fixture
def function_marked_bl_def_act(function) -> Function:
    function.mark_bl()
    function.mark_def()
    function.mark_act()
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
def test_simple(function_marked_bl_def_act):
    """
    `with` statement is part of arrange. Blank lines are maintained around Act.
    """
    result = function_marked_bl_def_act.mark_arrange()

    assert result == 1
    assert function_marked_bl_def_act.line_markers == [
        LineType.func_def,
        LineType.arrange,
        LineType.blank_line,
        LineType.act,
        LineType.blank_line,
        LineType.unprocessed,
    ]


@pytest.mark.parametrize(
    'code_str', [
        '''
def test_extra_arrange(hello_world_path):
    with open(hello_world_path) as f:
        f.read()

        result = f.read()

        assert not f.closed
    assert result == ''
'''
    ]
)
def test_extra(function_marked_bl_def_act):
    """
    Any extra arrangement goes in the `with` block.
    """
    result = function_marked_bl_def_act.mark_arrange()

    assert result == 2
    assert function_marked_bl_def_act.line_markers == [
        LineType.func_def,
        LineType.arrange,
        LineType.arrange,
        LineType.blank_line,
        LineType.act,
        LineType.blank_line,
        LineType.unprocessed,
        LineType.unprocessed,
    ]


@pytest.mark.parametrize(
    'code_str', [
        '''
def test_long_string():
    long_string = """

    """

    result = isinstance(long_string, str)

    assert result is True
'''
    ]
)
def test_bl_in_str(function_marked_bl_def_act):
    """
    String containing blank lines before Act is marked as Arrange
    """
    result = function_marked_bl_def_act.mark_arrange()

    assert result == 3
    assert function_marked_bl_def_act.line_markers == [
        LineType.func_def,
        LineType.arrange,
        LineType.arrange,
        LineType.arrange,
        LineType.blank_line,
        LineType.act,
        LineType.blank_line,
        LineType.unprocessed,
    ]
