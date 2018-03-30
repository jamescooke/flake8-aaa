import ast

import pytest

from flake8_aaa.function import Function
from flake8_aaa.helpers import find_test_functions, load_markers


@pytest.fixture
def function(code_str, file_tokens):
    """
    Args:
        code_str (str)

    Returns:
        Function
    """
    tree = ast.parse(code_str)
    function_node = find_test_functions(tree)[0]
    function = Function(function_node)
    function.pull_markers(load_markers(file_tokens))
    return function
