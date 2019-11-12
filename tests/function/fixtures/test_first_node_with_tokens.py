import ast

import pytest


@pytest.mark.parametrize('code_str', ['''
def test():
    pass  # act
'''])
def test(first_node_with_tokens):
    result = first_node_with_tokens

    assert result.name == 'test'
    assert len(result.body) == 1
    pass_node = result.body[0]
    assert isinstance(pass_node, ast.Pass)
    assert pass_node.first_token.line.strip().endswith('# act')
