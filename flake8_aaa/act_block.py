import ast
from typing import List, Type, TypeVar

from .helpers import node_is_pytest_raises, node_is_result_assignment, node_is_unittest_raises
from .types import ActBlockType

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
    def build_body(cls: Type[AB], body: List[ast.stmt]) -> List:
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
