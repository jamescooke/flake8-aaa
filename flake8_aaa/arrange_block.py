import ast
from typing import List

from .types import LineType


class ArrangeBlock:
    """
    Attributes:
        nodes (list (ast Node))
    """

    def __init__(self) -> None:
        self.nodes = []  # type: List[ast.AST]

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

    def mark_line_types(self, line_types: List[LineType], first_line_no: int) -> List[LineType]:
        """
        Mark lines occupied by this ArrangeBlock.

        Note:
            Mutates the ``line_types`` list.

        Raises:
            AssertionError: When position in ``line_types`` has already been
                marked to something other than ``???:unprocessed``.
        """
        # Lines calculated relative to file
        start_line = self.nodes[0].first_token.start[0]  # type:ignore
        end_line = self.nodes[-1].last_token.end[0]  # type:ignore
        for file_line_no in range(start_line, end_line + 1):
            assert line_types[file_line_no - first_line_no] is LineType.unprocessed
            line_types[file_line_no - first_line_no] = LineType.arrange_block
        return line_types
