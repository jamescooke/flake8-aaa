import ast

import asttokens
import pytest

from flake8_aaa.helpers import node_is_result_assignment


@pytest.mark.parametrize('code_str', (
    'result = 1',
    'result = lambda x: x + 1',
))
def test(code_str):
    tree = ast.parse(code_str)
    asttokens.ASTTokens(code_str, tree=tree)
    node = tree.body[0]

    result = node_is_result_assignment(node)

    assert result is True


@pytest.mark.parametrize(
    'code_str', (
        'xresult = 1',
        'result, _ = 1, 2',
        'result[0] = 0',
        'result += 1',
        'result -= 1',
    )
)
def test_no(code_str):
    tree = ast.parse(code_str)
    asttokens.ASTTokens(code_str, tree=tree)
    node = tree.body[0]

    result = node_is_result_assignment(node)

    assert result is False
