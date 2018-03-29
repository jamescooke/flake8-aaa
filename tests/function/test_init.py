import ast

import pytest

from flake8_aaa.function import Function
from flake8_aaa.helpers import find_test_functions


@pytest.fixture
def function_node():
    """
    Returns:
        ast.FunctionDef: A test function.
    """
    tree = ast.parse("""import pytest

# Do nothing :D

@pytest.fixture
def thing():
    return 'thing'


def test(thing):
    result = thing

    assert result == 'thing'
""")
    return find_test_functions(tree)[0]


# --- TESTS ---


def test(function_node):
    result = Function(function_node)

    assert result.node == function_node
    assert result.start_line == 10
    assert result.end_line == 13
    assert result.markers == {}
