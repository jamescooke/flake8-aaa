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
def test_simple(function_bl_cmt_def_act):
    """
    `with` statement is part of arrange. Blank lines are maintained around Act.
    """
    result = function_bl_cmt_def_act.mark_arrange()

    assert result == 1
    assert function_bl_cmt_def_act.line_markers.types == [
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
def test_extra(function_bl_cmt_def_act):
    """
    Any extra arrangement goes in the `with` block.
    """
    result = function_bl_cmt_def_act.mark_arrange()

    assert result == 2
    assert function_bl_cmt_def_act.line_markers.types == [
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
def test_bl_in_str(function_bl_cmt_def_act):
    """
    String containing blank lines before Act is marked as Arrange
    """
    result = function_bl_cmt_def_act.mark_arrange()

    assert result == 3
    assert function_bl_cmt_def_act.line_markers.types == [
        LineType.func_def,
        LineType.arrange,
        LineType.arrange,
        LineType.arrange,
        LineType.blank_line,
        LineType.act,
        LineType.blank_line,
        LineType.unprocessed,
    ]


@pytest.mark.parametrize('code_str', ['''
def test_addition():
    result = 1 + 3

    assert result == 4
'''])
def test_no_arrange(function_bl_cmt_def_act):
    """
    Function without arrange block does not cause failure
    """
    result = function_bl_cmt_def_act.mark_arrange()

    assert result == 0
    assert function_bl_cmt_def_act.line_markers.types == [
        LineType.func_def,
        LineType.act,
        LineType.blank_line,
        LineType.unprocessed,
    ]
