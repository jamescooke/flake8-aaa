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
def test(first_node_with_tokens: ast.AST) -> None:
    """
    `pytest.raises()` with statement is the Act node.
    """
    with_mock_node = first_node_with_tokens.body[1]
    with_pytest_node = with_mock_node.body[0]

    result = Block.build_act(
        node=with_pytest_node,
        test_func_node=first_node_with_tokens,
        act_block_style=ActBlockStyle.DEFAULT,
    )

    assert isinstance(result, Block)
    assert result.first_line_no == 8
    assert result.last_line_no == 9
    assert result.line_type == LineType.act
