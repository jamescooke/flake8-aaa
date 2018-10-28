import ast
from typing import List, Type, TypeVar

from .helpers import node_is_pytest_raises, node_is_result_assignment, node_is_unittest_raises
from .types import ActBlockType, LineType

AB = TypeVar('AB', bound='ActBlock')  # Place holder for ActBlock instances


class ActBlock:
    """
    Attributes:
        node
        block_type (ActBlockType)
    """

    def __init__(self, node: ast.AST, block_type: ActBlockType) -> None:
        """
        Args:
            node
            block_type (ActBlockType)
        """
        self.node = node  # type: ast.AST
        self.block_type = block_type  # type: ActBlockType

    @classmethod
    def build_body(cls: Type[AB], body: List[ast.stmt]):
        """
        Note:
            Return type is probably ``-> List[AB]``, but can't get it to pass.
        """
        act_blocks = []  # type: List[ActBlock]
        for child_node in body:
            act_blocks += ActBlock.build(child_node)
        return act_blocks

    @classmethod
    def build(cls: Type[AB], node: ast.AST) -> List[AB]:
        if node_is_result_assignment(node):
            return [cls(node, ActBlockType.result_assignment)]
        if node_is_pytest_raises(node):
            return [cls(node, ActBlockType.pytest_raises)]
        if node_is_unittest_raises(node):
            return [cls(node, ActBlockType.unittest_raises)]

        token = node.first_token  # type: ignore
        # Check if line marked with '# act'
        if token.line.strip().endswith('# act'):
            return [cls(node, ActBlockType.marked_act)]

        # Recurse if it's a context manager
        if isinstance(node, ast.With):
            return cls.build_body(node.body)

        return []

    def mark_line_types(self, line_types: List[LineType], first_line_no: int) -> List[LineType]:
        """
        Marks the lines occupied by this ActBlock.

        Note:
            Mutates the ``line_types`` list.

        Raises:
            AssertionError: When position in ``line_types`` has already been
                marked to something other than ``???:unprocessed``.
        """
        # Lines calculated relative to file
        start_line = self.node.first_token.start[0]  # type:ignore
        end_line = self.node.last_token.end[0]  # type:ignore
        for file_line_no in range(start_line, end_line + 1):
            assert line_types[file_line_no - first_line_no] is LineType.unprocessed
            line_types[file_line_no - first_line_no] = LineType.act_block
        return line_types
