import ast


class ArrangeBlock:
    """
    Attributes:
        nodes (list (ast Node))
    """

    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        """
        Add node if it's an "arrangement node".

        Returns:
            bool: Node is an arrangement node.
        """
        if isinstance(node, ast.Pass):
            return False
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            return False

        self.nodes.append(node)
        return True
