import ast
from typing import Iterable, List, Tuple, Type, TypeVar

from .conf import ActBlockStyle
from .exceptions import EmptyBlock
from .helpers import add_node_parents, filter_arrange_nodes, get_first_token, get_last_token
from .types import LineType

_Block = TypeVar('_Block', bound='Block')


class Block:
    """
    An Arrange, Act or Assert block of code as parsed from the test function.

    Act blocks are simply a single Act node in default mode. However, in a
    future version (update TODO200), "large" Act blocks will include the Act
    node and any context managers that wrap them.

    Note:
        Blocks with no nodes are allowed (at the moment).

    Args:
        nodes: Nodes that make up this block.
        line_type: Type of line that this blocks writes into the line markers
            instance for the function.
    """

    def __init__(self, nodes: Iterable[ast.AST], lt: LineType) -> None:
        self.nodes = tuple(nodes)
        self.line_type = lt

    @classmethod
    def build_act(
        cls: Type[_Block],
        node: ast.stmt,
        test_func_node: ast.FunctionDef,  # use this in TODO200
        act_block_style: ActBlockStyle,  # use this in TODO200
    ) -> _Block:
        """
        Act block is a single node by default. TODO200

        Args:
            node: Act node already found by Function.mark_act()
            test_func_node: Node of test function / method.
            act_block_style: Default Act Blocks are just the Act node. Large
                Act Blocks can absorb context managers that wrap them.
        """
        if act_block_style == ActBlockStyle.DEFAULT:
            return cls([node], LineType.act)

        # --- LARGE Act Block behaviour...

        add_node_parents(test_func_node)
        # Walk up the parent nodes of the parent node to find test's definition.
        act_block_node = node
        while act_block_node.parent != test_func_node:
            act_block_node = act_block_node.parent

        return cls([act_block_node], LineType.act)

    @classmethod
    def build_arrange(cls: Type[_Block], nodes: List[ast.stmt], act_block_first_line: int) -> _Block:
        """
        Arrange block is all non-pass and non-docstring nodes before the Act
        block start.

        Args:
            nodes: Body of test function / method.
            act_block_first_line
        """
        return cls(filter_arrange_nodes(nodes, act_block_first_line), LineType.arrange)

    def get_span(self, first_line_no: int) -> Tuple[int, int]:
        """
        Args:
            first_line_no: First line number of Block. Used to calculate
                relative line numbers.

        Returns:
            First and last line covered by this block, counted relative to the
            start of the Function.

        Raises:
            EmptyBlock: when block has no nodes
        """
        if not self.nodes:
            raise EmptyBlock(f'span requested from {self.line_type} block with no nodes')
        # start and end are (<line number>, <indent>) pairs, so just the line
        # numbers are picked out.
        return (
            get_first_token(self.nodes[0]).start[0] - first_line_no,
            get_last_token(self.nodes[-1]).end[0] - first_line_no,
        )
