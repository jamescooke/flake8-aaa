from .act_block import ActBlock
from .exceptions import NotActionBlock


class Function:
    """
    Attributes:
        act_blocks (list (ActBlock)): List of nodes that are considered Act
            blocks for this test. Defaults to ``None`` when function has not
            been parsed.
        node (astroid.FunctionDef): AST for the test under lint.
        tokens (asttokens.ASTTokens): Tokens for the file under test.
    """

    def __init__(self, node, tokens):
        """
        Args:
            node (ast.FunctionDef)
            tokens (asttokens.ASTTokens)
        """
        self.node = node
        self.tokens = tokens
        self.act_blocks = None

    def parse(self):
        """
        Processes the child nodes of ``node`` to find Act blocks which are kept
        in the ``act_blocks`` attribute.

        Returns:
            int: Number of Act blocks found.
        """
        self.act_blocks = []
        for child_node in self.node.get_children():
            try:
                self.act_blocks.append(ActBlock.build(child_node, self.tokens))
            except NotActionBlock:
                continue
        return len(self.act_blocks)

    def check(self):
        """
        Check test function for errors. Test functions that are just 'pass' are
        skipped.

        Returns:
            list (tuple): Errors in flake8 (line_number, offset, text)
        """
        return []
        return [
            (self.node.lineno, self.node.col_offset, 'AAA01 no result variable set in test'),
        ]
