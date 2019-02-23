import pytest

from flake8_aaa.block import Block
from flake8_aaa.types import LineType


def test_empty():
    result = Block([], LineType.act)

    assert result.nodes == ()
    assert result.line_type == LineType.act


@pytest.mark.parametrize(
    'code_str', [
        '''
def test():
    """
    Do some stuff
    """
    x = 1
    y = 2

    result = x + y

    assert result == 3
'''
    ]
)
def test_some(first_node_with_tokens):
    result = Block(first_node_with_tokens.body, LineType._assert)

    assert len(result.nodes) == 5
