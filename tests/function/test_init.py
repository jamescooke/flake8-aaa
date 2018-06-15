import pytest

from flake8_aaa.function import Function


@pytest.mark.parametrize('code_str', ['''
def test():
    pass
'''])
def test(first_node_with_tokens):
    result = Function(first_node_with_tokens)

    assert result.node == first_node_with_tokens
    assert result.act_block is None
