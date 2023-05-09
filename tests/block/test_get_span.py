import ast

import pytest

from flake8_aaa.block import get_span


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
def test(first_node_with_tokens: ast.FunctionDef) -> None:
    """
    For a block that contains the whole body of the test, first and last line
    numbers are returned.
    """
    result = get_span(first_node_with_tokens.body[0], first_node_with_tokens.body[-1])

    assert result == (6, 18)


@pytest.mark.parametrize('code_str', [
    '''
long_string = """

"""
    ''',
])
def test_context_arrange(first_node_with_tokens: ast.AST) -> None:
    """
    Long string spans are counted.
    """
    result = get_span(first_node_with_tokens, first_node_with_tokens)

    assert result == (2, 4)
