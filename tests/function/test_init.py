import asttokens
import pytest

from flake8_aaa.function import Function


@pytest.mark.parametrize('code_str', ['''
    def test():
        pass
    '''])
def test(function_node, code_str):
    tokens = asttokens.ASTTokens(code_str, tree=function_node)

    result = Function(function_node, tokens)

    assert result.node == function_node
    assert result.tokens == tokens
    assert result.act_blocks is None
