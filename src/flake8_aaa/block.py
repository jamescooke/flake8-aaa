import ast
from typing import Iterable, List, Tuple, Type, TypeVar

from .helpers import filter_arrange_nodes, filter_assert_nodes, get_first_token, get_last_token
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
    def build_arrange(cls: Type[_Block], nodes: List[ast.stmt], max_line_number: int) -> _Block:
        """
        Arrange block is all non-pass and non-docstring nodes before the Act
        block start.
        """
        return cls(filter_arrange_nodes(nodes, max_line_number), LineType.arrange_block)

    @classmethod
    def build_assert(cls: Type[_Block], nodes: List[ast.stmt], min_line_number: int) -> _Block:
        """
        Assert block is all nodes that are after the Act node.

        Note:
            The filtering is *still* running off the line number of the Act
            node, when instead it should be using the last line of the Act
            block.

            TODO: This case needs testing::

                with mock.patch(thing):
                    with pytest.raises(ValueError):
                        do_thing()
                    print('hi')

            Does the ``print('hi')`` get correctly grabbed by the Act Block?
        """
        return cls(filter_assert_nodes(nodes, min_line_number), LineType.assert_block)

    def get_span(self, first_line_no: int) -> Tuple[int, int]:
        assert self.nodes
        return (
            get_first_token(self.nodes[0]).start[0] - first_line_no,
            get_last_token(self.nodes[-1]).start[0] - first_line_no,
        )
