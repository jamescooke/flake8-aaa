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
    tree = ast.parse("""
def test():
    pass
""")
    return find_test_functions(tree)[0]


# --- TESTS ---


def test(function_node):
    result = Function(function_node)

    assert result.node == function_node
