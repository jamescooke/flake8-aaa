import ast
import re
from typing import List, Type, TypeVar

from .helpers import (
    get_first_token,
    get_last_token,
    node_is_pytest_context_manager,
    node_is_result_assignment,
    node_is_unittest_raises,
)
from .types import ActNodeType

AN = TypeVar('AN', bound='ActNode')  # Place holder for ActNode instances
act_pattern = re.compile('# act$', re.IGNORECASE)


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
        self.node = node
        self.block_type = block_type

    @classmethod
    def build_body(cls: Type[AN], body: List[ast.stmt]) -> List:
        """
        Note:
            Return type is probably ``-> List[AN]``, but can't get it to pass.
        """
        act_nodes: List[ActNode] = []
        for child_node in body:
            act_nodes += ActNode.build(child_node)
        return act_nodes

    @classmethod
    def build(cls: Type[AN], node: ast.stmt) -> List[AN]:
        """
        Starting at this ``node``, check if it's an act node. If it's a context
        manager, recurse into child nodes.

        Finds "# act" marked Act nodes where the marker is on the first or last
        line of the node.

        Returns:
            List of all act nodes found.
        """
        if node_is_result_assignment(node):
            return [cls(node, ActNodeType.result_assignment)]
        if node_is_pytest_context_manager(node):
            return [cls(node, ActNodeType.pytest_context_manager)]
        if node_is_unittest_raises(node):
            return [cls(node, ActNodeType.unittest_raises)]

        # Recurse (downwards) if it's a context manager - do this first before
        # looking for any '# act' marked blocks because otherwise strange
        # things happen with blocks like:
        #   with open(path) as f:
        #       f.do()  # act
        if isinstance(node, ast.With):
            return cls.build_body(node.body)

        # Check if first or last line is marked with '# act'
        if (
            act_pattern.search(get_first_token(node).line.strip())
            or act_pattern.search(get_last_token(node).line.strip())
        ):
            return [cls(node, ActNodeType.marked_act)]

        return []
