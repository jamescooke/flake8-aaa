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
def test_simple(function_bl_cmt_def):
    """
    `with` statement is part of arrange. Blank lines are maintained around Act.
    """
    result = function_bl_cmt_def.mark_act()

    assert result == 1
    assert function_bl_cmt_def.line_markers.types == [
        LineType.func_def,
        LineType.unprocessed,
        LineType.blank_line,
        LineType.act,
        LineType.blank_line,
        LineType.unprocessed,
    ]


@pytest.mark.parametrize(
    'code_str', [
        '''
def test_pytest_assert_raises_in_block(hello_world_path):
    with open(hello_world_path) as f:

        with pytest.raises(io.UnsupportedOperation):
            f.write('hello back')

        assert f.read() == 'Hello World!'
'''
    ]
)
def test_raises_block(function_bl_cmt_def):
    """
    Checking on a raise in a with block works with Pytest.
    """
    result = function_bl_cmt_def.mark_act()

    assert result == 2
    assert function_bl_cmt_def.line_markers.types == [
        LineType.func_def,
        LineType.unprocessed,
        LineType.blank_line,
        LineType.act,
        LineType.act,
        LineType.blank_line,
        LineType.unprocessed,
    ]


@pytest.mark.parametrize(
    'code_str', [
        '''
def test_pytest_assert_raises_in_block(hello_world_path):
    with open(hello_world_path) as f:

        with pytest.raises(io.UnsupportedOperation):
            # Write hello back to file
            f.write('hello back')

        assert f.read() == 'Hello World!'
'''
    ]
)
def test_raises_block_with_comment(function_bl_cmt_def):
    """
    Act block can be marked even though there is a comment in the middle of it
    """
    result = function_bl_cmt_def.mark_act()

    assert result == 3
    assert function_bl_cmt_def.line_markers.types == [
        LineType.func_def,
        LineType.unprocessed,
        LineType.blank_line,
        LineType.act,
        LineType.comment,
        LineType.act,
        LineType.blank_line,
        LineType.unprocessed,
    ]
