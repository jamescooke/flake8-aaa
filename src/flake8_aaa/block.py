import ast
from typing import Iterable, Set

from .helpers import build_footprint
from .types import LineType


class Block:
    """
    An Arrange, Act or Assert block of code as parsed from the test function.

    Args:
        nodes: Nodes that make up this block.
        line_type: Type of line that this blocks writes into the line markers
            instance for the function.

    Notes:
        * Blocks with no nodes are allowed (at the moment).
    """

    def __init__(self, nodes: Iterable[ast.AST], lt: LineType) -> None:
        self.nodes = tuple(nodes)
        self.line_type = lt

    def build_footprint(self, first_line_no: int) -> Set[int]:
        """
        Args:
            first_line_no: First line number of the function that contains this
                code block, so that the returned line numbers are all relative
                to the function definition which is at line 0.
        """
        out = set()  # type: Set[int]
        for node in self.nodes:
            out = out.union(build_footprint(node, first_line_no))
        return out
