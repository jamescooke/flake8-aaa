import pytest


@pytest.mark.parametrize('code_str', ["""
def test():
    pass  # AAA act
"""])
def test(function):
    result = function

    assert result.node.name == 'test'
    assert list(result.markers) == [3]
    assert result.markers[3].token.string == '# AAA act'
