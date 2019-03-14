import ast
from typing import Iterable, List, Tuple, Type, TypeVar

from .exceptions import EmptyBlock
from .helpers import add_node_parents, filter_arrange_nodes, filter_assert_nodes, get_first_token, get_last_token
from .types import LineType

_Block = TypeVar('_Block', bound='Block')


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

    @classmethod
    def build_act(cls: Type[_Block], node: ast.stmt, test_func_node: ast.FunctionDef) -> _Block:
        """
        Act block is a single node - either the act node itself, or the node
        that wraps the act node.
        """
        add_node_parents(test_func_node)
        # Walk up the parent nodes of the parent node to find test's definition.
        act_block_node = node
        while act_block_node.parent != test_func_node:  # type: ignore
            act_block_node = act_block_node.parent  # type: ignore
        return cls([act_block_node], LineType.act)

    @classmethod
    def build_arrange(cls: Type[_Block], nodes: List[ast.stmt], max_line_number: int) -> _Block:
        """
        Arrange block is all non-pass and non-docstring nodes before the Act
        block start.
        """
        return cls(filter_arrange_nodes(nodes, max_line_number), LineType.arrange)

    @classmethod
    def build_assert(cls: Type[_Block], nodes: List[ast.stmt], min_line_number: int) -> _Block:
        """
        Assert block is all nodes that are after the Act node.

        Note:
            The filtering is *still* running off the line number of the Act
            node, when instead it should be using the last line of the Act
            block.
        """
        return cls(filter_assert_nodes(nodes, min_line_number), LineType._assert)

    def get_span(self, first_line_no: int) -> Tuple[int, int]:
        """
        Raises:
            EmptyBlock: when block has no nodes
        """
        if not self.nodes:
            raise EmptyBlock('span requested from {} block with no nodes'.format(self.line_type))
        return (
            get_first_token(self.nodes[0]).start[0] - first_line_no,
            get_last_token(self.nodes[-1]).start[0] - first_line_no,
        )
