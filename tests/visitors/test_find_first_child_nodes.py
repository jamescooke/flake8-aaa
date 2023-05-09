import pytest

from flake8_aaa.visitors import find_first_child_nodes


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
def test(first_node_with_tokens) -> None:
    with_mock_node = first_node_with_tokens.body[0]
    with_pytest_node = with_mock_node.body[0]
    things_node = with_pytest_node.body[0]

    result = find_first_child_nodes(first_node_with_tokens)

    assert result == {
        with_pytest_node: with_mock_node,
        things_node: with_pytest_node,
    }


@pytest.mark.parametrize(
    'code_str', [
        '''
def test_extra_arrange(hello_world_path: pathlib.Path) -> None:
    with open(hello_world_path) as f:
        f.read()

        result = f.read()

    assert result == ''
'''
    ]
)
def test_not_first_child(first_node_with_tokens) -> None:
    with_open_node = first_node_with_tokens.body[0]
    f_read_node = with_open_node.body[0]

    result = find_first_child_nodes(first_node_with_tokens)

    assert result == {
        f_read_node: with_open_node,
    }
