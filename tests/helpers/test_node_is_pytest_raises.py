import ast

import asttokens
import pytest

from flake8_aaa.helpers import node_is_pytest_raises


@pytest.mark.parametrize(
    'code_str', [
        '''
def test():
    with pytest.raises(Exception):
        do_thing()
''',
        '''
def test_other():
    with pytest.raises(Exception) as excinfo:
        do_thing()
''',
    ]
)
def test(first_node_with_tokens):
    with_node = first_node_with_tokens.body[0]

    result = node_is_pytest_raises(with_node)

    assert result is True


@pytest.mark.parametrize('code_str', [
    '''with open('test.txt') as f:
    f.read()''',
])
def test_no(code_str):
    tree = ast.parse(code_str)
    asttokens.ASTTokens(code_str, tree=tree)
    node = tree.body[0]

    result = node_is_pytest_raises(node)

    assert result is False
