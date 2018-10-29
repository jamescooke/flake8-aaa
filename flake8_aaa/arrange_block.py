import ast
from typing import List  # noqa

from .multi_node_block import MultiNodeBlock
from .types import LineType


class ArrangeBlock(MultiNodeBlock):
    line_type = LineType.arrange_block

    def add_node(self, node: ast.AST) -> bool:
        """
        Add node if it's an "arrangement node".
        """
        if isinstance(node, ast.Pass):
            return False
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            return False

        self.nodes.append(node)
        return True
