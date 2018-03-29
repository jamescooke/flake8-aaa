import ast

import pytest

from flake8_aaa.function import Function
from flake8_aaa.helpers import find_test_functions


@pytest.fixture
def function(code_str):
    """
    Args:
        code_str (str)

    Returns:
        Function
    """
    tree = ast.parse(code_str)
    function_node = find_test_functions(tree)[0]
    return Function(function_node)
