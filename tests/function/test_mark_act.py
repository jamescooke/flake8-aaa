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

    result = function.mark_act()

    assert result == 1
    assert function.line_markers.types == [
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
def test_raises_block(function):
    """
    Checking on a raise in a with block works with Pytest.
    """
    function.mark_bl()
    function.mark_def()

    result = function.mark_act()

    assert result == 2
    assert function.line_markers.types == [
        LineType.func_def,
        LineType.unprocessed,
        LineType.blank_line,
        LineType.act,
        LineType.act,
        LineType.blank_line,
        LineType.unprocessed,
    ]
