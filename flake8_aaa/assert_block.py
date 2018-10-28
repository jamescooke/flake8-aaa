import ast

from .multi_node_block import MultiNodeBlock
from .types import LineType


class AssertBlock(MultiNodeBlock):
    line_type = LineType.assert_block

    def add_node(self, node: ast.AST) -> bool:
        self.nodes.append(node)
        return True
