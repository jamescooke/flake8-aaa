import ast

from flake8_aaa.act_node import ActNode
from flake8_aaa.types import ActNodeType


def test():
    node = ast.parse('result = do_thing()').body[0]

    result = ActNode(node, ActNodeType.result_assignment)

    assert result.node == node
    assert result.block_type == ActNodeType.result_assignment
