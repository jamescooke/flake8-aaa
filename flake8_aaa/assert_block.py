class AssertBlock:
    """
    Attributes:
        nodes (list (ast Node))
    """

    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)
