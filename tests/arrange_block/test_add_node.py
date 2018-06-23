import pytest

from flake8_aaa.arrange_block import ArrangeBlock
from flake8_aaa.function import Function


@pytest.fixture
def function(first_node_with_tokens, lines):
    """
    Returns:
        Function: Loaded with ``first_node_with_tokens`` node, lines of test
        are passed to Function.
    """
    return Function(first_node_with_tokens, lines)


# --- TESTS ---


@pytest.mark.parametrize(
    'code_str',
    ['''
def test():
    x = 1
'''],
    ids=['assignment'],
)
def test(function):
    arrange_block = ArrangeBlock()

    result = arrange_block.add_node(function.node.body[0])

    assert result is True
    assert arrange_block.nodes == [function.node.body[0]]


@pytest.mark.parametrize(
    'code_str',
    ['''
def test():
    """
    Do nothing
    """
''', '''
def test():
    pass
'''],
    ids=['docstring', 'pass'],
)
def test_not_loaded(function):
    arrange_block = ArrangeBlock()

    result = arrange_block.add_node(function.node.body[0])

    assert result is False
    assert len(arrange_block.nodes) == 0
