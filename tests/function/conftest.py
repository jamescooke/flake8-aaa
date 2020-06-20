import pytest

from flake8_aaa.function import Function


@pytest.fixture
def function(first_node_with_tokens, lines, tokens) -> Function:
    """
    Returns:
        Loaded with ``first_node_with_tokens`` node, lines of test are passed
        to Function.
    """
    return Function(first_node_with_tokens, lines, tokens)
