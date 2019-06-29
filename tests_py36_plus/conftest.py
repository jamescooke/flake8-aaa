import ast

import asttokens
import pytest


@pytest.fixture
def first_node_with_tokens(code_str):
    """
    Given ``code_str`` fixture, parse that string with ``ast.parse`` and then
    augment it with ``asttokens.ASTTokens``.

    Returns:
        ast.node: First node in parsed tree.
    """
    tree = ast.parse(code_str)
    asttokens.ASTTokens(code_str, tree=tree)
    return tree.body[0]
