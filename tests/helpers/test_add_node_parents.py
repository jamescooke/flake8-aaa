import pytest

from flake8_aaa.helpers import add_node_parents


@pytest.mark.parametrize(
    'code_str', [
        '''
def test():
    with mock.patch('things.thinger'):
        with pytest.raises(ValueError):
            things()
'''
    ]
)
def test(first_node_with_tokens):
    with_mock_node = first_node_with_tokens.body[0]
    with_pytest_node = with_mock_node.body[0]

    result = add_node_parents(first_node_with_tokens)

    assert result is None
    assert with_pytest_node.parent == with_mock_node
    assert with_mock_node.parent == first_node_with_tokens
