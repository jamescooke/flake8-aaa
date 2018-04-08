import pytest
import astroid


@pytest.mark.parametrize('code_str', ["""
def test():
    pass  # act
"""])
def test(function):
    result = function

    assert result.node.name == 'test'
    pass_node = list(result.node.get_children())[-1]
    assert isinstance(pass_node, astroid.Pass)
    first_pass_token = next(result.tokens.get_tokens(pass_node, include_extra=True))
    assert first_pass_token.line.strip().endswith('# act')
