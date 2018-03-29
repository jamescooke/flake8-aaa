import ast


class Function:
    """
    Attributes:
        node (ast.FunctionDef): AST for the test under lint.
        start_line (int): First line of test.
        end_line (int): Last line of test.
    """

    def __init__(self, node):
        """
        Args:
            node (ast.FunctionDef)
        """
        self.node = node
        self.start_line = self.node.lineno
        self.end_line = self.node.body[-1].lineno

    def check(self):
        """
        Check test function for errors. Test functions that are just 'pass' are
        skipped.

        Returns:
            list (tuple): Errors in flake8 (line_number, offset, text)
        """
        if len(self.node.body) == 1:
            if isinstance(self.node.body[0], ast.Pass):
                return []

        for node in self.node.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                if isinstance(target, ast.Name) and target.id == 'result':
                    return []

        return [
            (node.lineno, node.col_offset, 'AAA01 no result variable set in test'),
        ]
