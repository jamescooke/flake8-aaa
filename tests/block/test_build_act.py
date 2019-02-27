import pytest

from flake8_aaa.block import Block
from flake8_aaa.types import LineType


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

    result = Block.build_act(with_pytest_node, first_node_with_tokens)

    assert result.nodes == (with_mock_node, )
    assert result.line_type == LineType.act_block
