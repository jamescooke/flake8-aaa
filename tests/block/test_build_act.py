import pytest

from flake8_aaa.block import Block
from flake8_aaa.conf import ActBlockStyle
from flake8_aaa.types import LineType


@pytest.mark.parametrize(
    'code_str', [
        '''
def test():
    with mock.patch('things.thinger'):
        with pytest.raises(ValueError):  # <-- Act block starts here with Default
            things()
'''
    ]
)
def test(first_node_with_tokens) -> None:
    """
    `pytest.raises()` with statement is the Act node.
    """
    with_mock_node = first_node_with_tokens.body[0]
    with_pytest_node = with_mock_node.body[0]

    result = Block.build_act(with_pytest_node, first_node_with_tokens, ActBlockStyle.DEFAULT)

    assert result.nodes == (with_pytest_node, )
    assert result.line_type == LineType.act


@pytest.mark.parametrize(
    'code_str', [
        '''
def test():
    with mock.patch('things.thinger'):  # <-- Act block starts here with Large
        with pytest.raises(ValueError):
            things()
'''
    ]
)
def test_large(first_node_with_tokens) -> None:
    """
    Large Act blocks absorb statements that contain them
    """
    with_mock_node = first_node_with_tokens.body[0]
    with_pytest_node = with_mock_node.body[0]

    result = Block.build_act(with_pytest_node, first_node_with_tokens, ActBlockStyle.LARGE)

    assert result.nodes == (with_mock_node, )
    assert result.line_type == LineType.act
