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


@pytest.fixture
def function_with_arrange_act_blocks(function_with_act_block):
    """
    Returns:
        Function: With Arrange and Act blocks loaded.
    """
    function_with_act_block.arrange_block = function_with_act_block.load_arrange_block()
    return function_with_act_block


@pytest.fixture
def function_aaa_blocks(function_with_arrange_act_blocks):
    """
    Returns:
        Function: With Arrange, Act, Assert blocks loaded.
    """
    function_with_arrange_act_blocks.assert_block = function_with_arrange_act_blocks.load_assert_block()
    return function_with_arrange_act_blocks
