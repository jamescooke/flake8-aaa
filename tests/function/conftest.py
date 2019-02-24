import pytest

from flake8_aaa.function import Function


@pytest.fixture
def function(first_node_with_tokens, lines) -> Function:
    """
    Returns:
        Loaded with ``first_node_with_tokens`` node, lines of test are passed
        to Function.
    """
    return Function(first_node_with_tokens, lines)


@pytest.fixture
def function_with_act_block(function):
    """
    Returns:
        Function: With Act block loaded.
    """
    function.check_act()
    return function
