import pytest

from flake8_aaa.block import Block
from flake8_aaa.types import LineType


@pytest.mark.parametrize(
    'code_str', [
        '''
def some_func():
    # This is completely un-linted :( - but good for testing :)
    with open('data.txt') as f:
        data = f.read()

    other_thing(data)

    push_to_service(data)
    return True
'''
    ]
)
def test(first_node_with_tokens):
    block = Block(first_node_with_tokens.body, LineType.assert_block)

    result = block.build_footprint(2)

    assert result == set((
        # 1, Comment line
        2,
        3,
        # 4, Blank line with no node
        5,
        # 6, Blank line with no node
        7,
        8,
    ))
