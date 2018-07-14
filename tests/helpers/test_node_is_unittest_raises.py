import ast

import asttokens
import pytest

from flake8_aaa.helpers import node_is_unittest_raises


@pytest.mark.parametrize(
    'code_str', [
        '''
def test(self):
    with self.assertRaises(IntegrityError) as cm:
        do_thing()
''',
        '''
def test_other(self):
    with self.assertRaises(ValueError) as cm:
        do_thing()
''',
    ]
)
def test(first_node_with_tokens):
    with_node = first_node_with_tokens.body[0]

    result = node_is_unittest_raises(with_node)

    assert result is True


@pytest.mark.parametrize('code_str', [
    '''with open('test.txt') as f:
    f.read()''',
])
def test_no(code_str):
    tree = ast.parse(code_str)
    asttokens.ASTTokens(code_str, tree=tree)
    node = tree.body[0]

    result = node_is_unittest_raises(node)

    assert result is False
