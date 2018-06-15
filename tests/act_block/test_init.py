import ast

from flake8_aaa.act_block import ActBlock
from flake8_aaa.types import ActBlockType


def test():
    node = ast.parse('result = do_thing()').body[0]

    result = ActBlock(node, ActBlockType.result_assignment)

    assert result.node == node
    assert result.block_type == ActBlockType.result_assignment
