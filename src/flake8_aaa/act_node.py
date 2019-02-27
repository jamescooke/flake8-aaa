import ast
from typing import List, Type, TypeVar

from .helpers import node_is_pytest_raises, node_is_result_assignment, node_is_unittest_raises
from .types import ActNodeType

AN = TypeVar('AN', bound='ActNode')  # Place holder for ActNode instances


class ActNode:
    """
    Attributes:
        node
        block_type
    """

    def __init__(self, node: ast.stmt, block_type: ActNodeType) -> None:
        """
        Args:
            node
            block_type
        """
        self.node = node  # type: ast.stmt
        self.block_type = block_type  # type: ActNodeType

    @classmethod
    def build_body(cls: Type[AN], body: List[ast.stmt]) -> List:
        """
        Note:
            Return type is probably ``-> List[AN]``, but can't get it to pass.
        """
        act_nodes = []  # type: List[ActNode]
        for child_node in body:
            act_nodes += ActNode.build(child_node)
        return act_nodes

    @classmethod
    def build(cls: Type[AN], node: ast.stmt) -> List[AN]:
        """
        Starting at this ``node``, check if it's an act node. If it's a context
        manager, recurse into child nodes.

        Returns:
            List of all act nodes found.
        """
        if node_is_result_assignment(node):
            return [cls(node, ActNodeType.result_assignment)]
        if node_is_pytest_raises(node):
            return [cls(node, ActNodeType.pytest_raises)]
        if node_is_unittest_raises(node):
            return [cls(node, ActNodeType.unittest_raises)]

        token = node.first_token  # type: ignore
        # Check if line marked with '# act'
        if token.line.strip().endswith('# act'):
            return [cls(node, ActNodeType.marked_act)]

        # Recurse (downwards) if it's a context manager
        if isinstance(node, ast.With):
            return cls.build_body(node.body)

        return []
