import ast
from typing import Dict


class FirstChildFinder(ast.NodeVisitor):
    """
    When building Large style act blocks, we need to know if any particular act
    node is the "first" child of a context manager. If it _is_, then the
    context manager can join the act block.

    Builds `_child_parent` dict which maps child node to parent node. This
    allows the act block builder to check if the act node is a first child
    using the key, and if so, it then has the parent so can recurse upwards.
    """

    def __init__(self) -> None:
        super().__init__()
        self.child_parent: Dict[ast.AST, ast.With] = {}

    def visit_With(self, node: ast.With) -> None:
        self.child_parent[node.body[0]] = node
        for child_node in node.body:
            self.visit(child_node)


def find_first_child_nodes(tree: ast.AST) -> Dict[ast.AST, ast.With]:
    """
    Wrapper for FirstChildFinder visitor - see docstring above
    """
    first_child_finder = FirstChildFinder()
    first_child_finder.visit(tree)
    return first_child_finder.child_parent
