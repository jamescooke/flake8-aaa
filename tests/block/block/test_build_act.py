import ast

import pytest

from flake8_aaa.block import Block
from flake8_aaa.conf import ActBlockStyle
from flake8_aaa.types import LineType


@pytest.mark.parametrize(
    'code_str', [
        '''# Line 1

def test():  # Line 3
    """
    Docstring helps to create space for offset calculation
    """
    with mock.patch('things.thinger'):
        with pytest.raises(ValueError):
            things()

# Line 11
'''
    ]
)
def test(first_node_with_tokens: ast.FunctionDef) -> None:
    """
    `pytest.raises()` with statement is the Act node.
    """
    with_mock_node = first_node_with_tokens.body[1]
    with_pytest_node = with_mock_node.body[0]  # type: ignore[attr-defined]

    result = Block.build_act(
        node=with_pytest_node,
        test_func_node=first_node_with_tokens,
        act_block_style=ActBlockStyle.DEFAULT,
    )

    assert isinstance(result, Block)
    assert result.first_line_no == 8
    assert result.last_line_no == 9
    assert result.line_type == LineType.act


@pytest.mark.parametrize(
    'code_str', [
        '''
def test():  # line 2
    with mock.patch('things.thinger'):  # <-- Act block starts here with Large
        with pytest.raises(ValueError):
            things()
'''
    ]
)
def test_large_first_child(first_node_with_tokens: ast.FunctionDef) -> None:
    """
    Large Act blocks absorb statements that contain them when Act node is first
    child of the wrapping context manager.
    """
    with_mock_node = first_node_with_tokens.body[0]
    with_pytest_node = with_mock_node.body[0]  # type: ignore[attr-defined]

    result = Block.build_act(
        node=with_pytest_node,
        test_func_node=first_node_with_tokens,
        act_block_style=ActBlockStyle.LARGE,
    )

    assert isinstance(result, Block)
    assert result.first_line_no == 3
    assert result.last_line_no == 5
    assert result.line_type == LineType.act


@pytest.mark.parametrize(
    'code_str', [
        '''
def test():
    with open('somefile.txt') as f:
        f.read()

        result = check_state(f)  # line 6

    assert result is False
'''
    ]
)
def test_large_second_child(first_node_with_tokens: ast.FunctionDef) -> None:
    """
    Large style Act block *don't* absorb context managers that are one or more
    lines of code "away". In this case, the Act block is not the first child.
    """
    with_open_node = first_node_with_tokens.body[0]
    result_assignment = with_open_node.body[1]  # type: ignore[attr-defined]

    result = Block.build_act(
        node=result_assignment,
        test_func_node=first_node_with_tokens,
        act_block_style=ActBlockStyle.LARGE,
    )

    assert isinstance(result, Block)
    assert result.first_line_no == 6
    assert result.last_line_no == 6
    assert result.line_type == LineType.act
