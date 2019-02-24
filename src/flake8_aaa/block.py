import ast
from typing import Iterable, Set, Type, TypeVar

from .helpers import build_footprint, filter_assert_nodes
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
    def build_assert(cls: Type[_Block], nodes: Iterable[ast.AST], min_line_number: int) -> _Block:
        """
        Assert block is all nodes that are after the Act node. Internal
        ``assert_block`` attr is set with the created ``Block``.

        Note:
            TODO: This case needs testing::

                with mock.patch(thing):
                    with pytest.raises(ValueError):
                        do_thing()
                    print('hi')

            Does the ``print('hi')`` get correctly grabbed by the Act Block?
        """
        return cls(filter_assert_nodes(nodes, min_line_number), LineType.assert_block)

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
