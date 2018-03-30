import ast

import six


class Function:
    """
    Attributes:
        node (ast.FunctionDef): AST for the test under lint.
        start_line (int): First line of test.
        end_line (int): Last line of test.
        markers (dict): Comment markers for this function. Loaded with
            ``pull_markers``.
    """

    def __init__(self, node):
        """
        Args:
            node (ast.FunctionDef)
        """
        self.node = node
        self.start_line = self.node.lineno
        self.end_line = self.node.body[-1].lineno
        self.markers = {}

    def pull_markers(self, all_markers):
        """
        Pull any comment markers.

        Args:
            all_markers (dict)

        Returns:
            int: Number of markers found for this function.

        Warning:
            Side effect: Updates ``self.markers`` with markers found.
        """
        for key, value in six.iteritems(all_markers):
            if self.start_line <= key and key <= self.end_line:
                self.markers[key] = value
        return len(self.markers)

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

        # For now assume that if any marker is found it's for the Act block,
        # wherever it is in the function.
        if len(self.markers):
            return []

        return [
            (node.lineno, node.col_offset, 'AAA01 no result variable set in test'),
        ]
