import pytest

from flake8_aaa.block import Block
from flake8_aaa.types import LineType


@pytest.mark.parametrize('code_str', ['''
def test():  # line 2
    result = 1  # line 3

    assert result == 1
'''])
def test_none(first_node_with_tokens):
    result = Block.build_arrange(first_node_with_tokens.body, 3)

    assert isinstance(result, Block)
    assert result.nodes == ()
    assert result.line_type == LineType.arrange


@pytest.mark.parametrize(
    'code_str', ['''
def test():
    x = 1
    y = 1

    result = x + y  # line 6

    assert result == 2
''']
)
def test_simple(first_node_with_tokens):
    result = Block.build_arrange(first_node_with_tokens.body, 6)

    assert len(result.nodes) == 2
    assert 'x = 1' in result.nodes[0].first_token.line
    assert 'y = 1' in result.nodes[1].first_token.line
