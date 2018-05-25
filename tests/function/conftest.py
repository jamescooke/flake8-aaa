import ast

import asttokens
import pytest

from flake8_aaa.function import Function


@pytest.fixture
def function_node(code_str):
    """
    Args:
        code_str (str): Should contain only one function which can be
            extracted.

    Returns:
        ast.FunctionDef
    """
    function_tree = ast.parse(code_str)
    return function_tree.body[0]


@pytest.fixture
def function(function_node, code_str):
    """
    Args:
        function_node (ast.FunctionDef)
        code_str (str)

    Returns:
        Function
    """
    tokens = asttokens.ASTTokens(code_str, tree=function_node)
    return Function(function_node, tokens)
