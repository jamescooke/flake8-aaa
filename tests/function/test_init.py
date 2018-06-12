import pytest

from flake8_aaa.function import Function


@pytest.mark.parametrize('code_str', ['''
def test():
    pass
'''])
def test(first_node_with_tokens, lines):
    result = Function(first_node_with_tokens)
    import ipdb
    ipdb.set_trace()

    assert result.node == first_node_with_tokens
    assert result.act_blocks == []
    assert result.parsed is False
    assert result.is_noop is False
