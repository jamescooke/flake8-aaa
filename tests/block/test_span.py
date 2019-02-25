import pytest

from flake8_aaa.block import Block
from flake8_aaa.types import LineType


def test_none():
    """
    Block must have nodes
    """
    block = Block([], LineType.act_block)

    with pytest.raises(AssertionError):
        block.get_span(13)


@pytest.mark.parametrize(
    'code_str', [
        '''
# Check first token and last token line numbers of the first and last lines
# (which span multiple lines). The whole test body is passed into the block.

def test():  # Line 5
    x = (
        1,
        2,
    )

    result = x + (3, 4)

    assert result == (
        1,
        2,
        3,
        4,
    )  # Line 18
'''
    ]
)
def test(first_node_with_tokens):
    block = Block(first_node_with_tokens.body, LineType.assert_block)

    result = block.get_span(5)

    assert result == (1, 13)
