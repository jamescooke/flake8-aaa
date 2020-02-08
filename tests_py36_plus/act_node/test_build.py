import pytest

from flake8_aaa.act_node import ActNode
from flake8_aaa.types import ActNodeType


@pytest.mark.parametrize(
    'code_str, expected_type', [
        ('result: Thing = do_thing()', ActNodeType.result_assignment),
        ('result: List[int] = do_thing()', ActNodeType.result_assignment),
    ]
)
def test(expected_type, first_node_with_tokens):
    """
    Assert that type-hinted result assignments can be found as act blocks
    """
    result: ActNode = ActNode.build(first_node_with_tokens)

    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], ActNode)
    assert result[0].node == first_node_with_tokens
    assert result[0].block_type == expected_type
