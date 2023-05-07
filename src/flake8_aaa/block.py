import ast
from typing import List, Tuple, Type, TypeVar

from .conf import ActBlockStyle
from .helpers import filter_arrange_nodes, get_first_token, get_last_token
from .types import LineType

_Block = TypeVar('_Block', bound='Block')


class Block:
    """
    An Arrange, Act or Assert block of code as parsed from the test function.

    A block is simply a group of lines in the test function along with their
    line type. It is represented by start and end line numbers relative to the
    test function.

    Note:
        TODO200: check on this. Can it be required that all blocks have at
        least one line?
        Blocks with no nodes are allowed (at the moment).

    Attributes:
        first_line_no
        last_line_no: Last line number *inclusive*. So a one line Block
            will have the same first and last line number.
        line_type: Type of line that this blocks writes into the line markers
            instance for the function.
    """

    def __init__(self, first_line_no: int, last_line_no: int, lt: LineType) -> None:
        assert first_line_no > 0, 'Got first_line_no for Block which is before function start'
        assert first_line_no <= last_line_no, 'Got last_line_no which is before first_line_no'
        self.first_line_no = first_line_no
        self.last_line_no = last_line_no
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
            act_block_style: Currently always DEFAULT. TODO200
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


def get_span(first_node: ast.AST, last_node: ast.AST, func_first_line_no: int) -> Tuple[int, int]:
    """
    Calculate first and last line covered by first and last nodes provided,
    counted relative to the start of the Function. The intention is that
    either:

    * Both nodes are the same and their span is calculated.

    * The nodes are the first of a block and the last of the block and they are
      checked to provide the span of the block.

    Args:
        nodes: Nodes from test function. When passing two nodes, they must be
            in order they appear in the code.
        func_first_line_no: First line number of Block. Used to calculate
            relative line numbers.
    """
    # start and end are (<line number>, <indent>) pairs, so just the line
    # numbers are picked out.
    return (
        get_first_token(first_node).start[0] - func_first_line_no,
        get_last_token(last_node).end[0] - func_first_line_no,
    )
