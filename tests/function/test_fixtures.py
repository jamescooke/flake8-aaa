import ast

import pytest

from flake8_aaa.helpers import get_first_token, get_last_token


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


@pytest.mark.parametrize(
    'code_str', ['''
@unittest.skip('not today')
def test(self):
    self.fail('should not happen')
''']
)
def test_function_start(function):
    """
    Assert function fixture includes decorations
    """
    result = get_first_token(function.node).line

    assert result == "@unittest.skip('not today')\n"


@pytest.mark.parametrize(
    'code_str', ['''
@unittest.skip('not today')
def test(self):
    self.fail('should not happen')
''']
)
def test_function_end(function):
    """
    Assert function with decoractors continues through the whole function
    """
    result = get_last_token(function.node).line

    assert result == "    self.fail('should not happen')\n"
