import ast
from typing import List, Tuple, Type, TypeVar

from .conf import ActBlockStyle
from .exceptions import EmptyBlock
from .helpers import filter_arrange_nodes, get_first_token, get_last_token
from .types import LineType
from .visitors import find_first_child_nodes

_Block = TypeVar('_Block', bound='Block')


class Block:
    """
    An Arrange, Act or Assert block of code as parsed from the test function.

    A Block is simply a group of lines in the test function. It has start and
    end line numbers (inclusive), along with line type.

    Note:
        All Blocks require at least one line. If an empty block is discovered
        while building, this is passed as the ``EmptyBlock`` exception.

    Attributes:
        first_line_no: First line of Block inclusive.
        last_line_no: Last line of Block inclusive..
        line_type: Type of line that this blocks writes into the line markers
            instance for the function.
    """

    def __init__(self, first_line_no: int, last_line_no: int, lt: LineType) -> None:
        assert first_line_no > 0, 'First line before start of file'
        assert first_line_no <= last_line_no, 'Got last line is before first line of Block'
        self.first_line_no = first_line_no
        self.last_line_no = last_line_no
        self.line_type = lt

    @classmethod
    def build_act(
        cls: Type[_Block],
        node: ast.stmt,
        test_func_node: ast.FunctionDef,
        act_block_style: ActBlockStyle,
    ) -> _Block:
        """
        Using the provided `node` as Act Node, build the Act Block depending on
        the `act_block_style`.

        Act blocks are simply a single Act node in default mode. However,
        "large" Act blocks include the Act node and any context managers that
        wrap them.

        Args:
            node: Act node already found by Function.mark_act()
            test_func_node: Node of test function / method.
            act_block_style: Default Act Blocks are just the Act node. Large
                Act Blocks can absorb context managers that wrap them.
        """
        if act_block_style == ActBlockStyle.DEFAULT:
            first, last = get_span(node, node)
            return cls(first, last, LineType.act)

        # --- LARGE Act Block behaviour...

        # Walk up the parent nodes of the act node, but only when act node is
        # the first child. This allows act block to absorb context managers
        # that have the act node first in their body.
        child_parent_map = find_first_child_nodes(test_func_node)
        wrapper_node = node
        while True:
            try:
                wrapper_node = child_parent_map[wrapper_node]
            except KeyError:
                break

        first, last = get_span(wrapper_node, node)
        return cls(first, last, LineType.act)

    @classmethod
    def build_arrange(cls: Type[_Block], nodes: List[ast.stmt], act_block_first_line: int) -> _Block:
        """
        Arrange block is all non-pass and non-docstring nodes before the Act
        block start.

        Args:
            nodes: Body of test function / method.
            act_block_first_line

        Raises:
            EmptyBlock: When no arrange nodes are found, there is no Arrange
                Block.
        """
        nodes = filter_arrange_nodes(nodes, act_block_first_line)
        if not nodes:
            raise EmptyBlock()

        first, last = get_span(nodes[0], nodes[-1])
        return cls(first, last, LineType.arrange)


def get_span(first_node: ast.AST, last_node: ast.AST) -> Tuple[int, int]:
    """
    Generate span of a Block as line numbers.

    First and last line covered by first and last nodes provided. The intention
    is that either:

    * For Blocks with a single node, that node is passed as first and last
      node. Therefore both nodes are the same and their span is calculated.

    * For Blocks with multiple nodes, the first and last of the Block are
      checked to provide the span of the Block. The caller has to manage which
      is the first and last node.

    Args:
        first_node: First node in Block.
        last_node: Last node in Block.
    """
    # start and end are (<line number>, <indent>) pairs, so just the line
    # numbers are picked out.
    return (
        get_first_token(first_node).start[0],
        get_last_token(last_node).end[0],
    )
