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


@pytest.mark.parametrize(
    'code_str', [
        '''
def some_func():  # line 2
    with open('data.txt') as f:  # line 3  (first node starts)
        with pytest.raises(ReadError):
            data = f.read()

        other_thing(data)

        push_to_service(data)  # line 9  (first node ends)

    return True  # Not in the first node
'''
    ]
)
def test_wrapped(first_node_with_tokens):
    """
    Asserts that the footprint calculation catches the "hanging nodes" that are
    still within the ``open()`` context manager. This could potentially happen
    with an Act block.
    """
    block = Block([first_node_with_tokens.body[0]], LineType.assert_block)

    result = block.build_footprint(2)

    assert result == set((
        1,  # with open(...)
        2,
        3,
        4,
        5,
        6,
        7,  # push_to_service()
    ))
