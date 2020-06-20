import ast
from typing import Iterable, List, Tuple, Type, TypeVar

from .exceptions import EmptyBlock
from .helpers import filter_arrange_nodes, get_first_token, get_last_token
from .types import LineType

_Block = TypeVar('_Block', bound='Block')


class Block:
    """
    An Arrange, Act or Assert block of code as parsed from the test function.

    Note:
        This may just become the Act Block *AND* since the Act Block is just a
        single node, this might not even be required.

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
    def build_act(cls: Type[_Block], node: ast.stmt) -> _Block:
        """
        Act block is a single node.
        """
        return cls([node], LineType.act)

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
