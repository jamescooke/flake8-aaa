from .act_block import ActBlock
from .exceptions import FunctionNotParsed, NotActionBlock
from .helpers import function_is_noop


class Function:
    """
    Attributes:
        act_blocks (list (ActBlock)): List of nodes that are considered Act
            blocks for this test. Defaults to ``None`` when function has not
            been parsed.
        node (astroid.FunctionDef): AST for the test under lint.
        tokens (asttokens.ASTTokens): Tokens for the file under test.
        is_noop (bool): Function is considered empty. Consists just of comments
            or ``pass``.
        parsed (bool): Function's nodes have been parsed.
    """

    def __init__(self, node, tokens):
        """
        Args:
            node (ast.FunctionDef)
            tokens (asttokens.ASTTokens)
        """
        self.node = node
        self.tokens = tokens
        self.act_blocks = []
        self.is_noop = False
        self.parsed = False

    def parse(self):
        """
        Processes the child nodes of ``node`` to find Act blocks which are kept
        in the ``act_blocks`` attribute. Sets ``parsed`` to ``True``.

        Returns:
            int: Number of Act blocks found.
        """
        self.act_blocks = []

        if function_is_noop(self.node):
            self.parsed = True
            self.is_noop = True
            return 0

        for child_node in self.node.get_children():
            try:
                self.act_blocks.append(ActBlock.build(child_node, self.tokens))
            except NotActionBlock:
                continue

        self.parsed = True
        return len(self.act_blocks)

    def check(self):
        """
        Check test function for errors.

        Returns:
            list (tuple): Errors in flake8 (line_number, offset, text)

        Raises:
            FunctionNotParsed: When ``parse`` has not been called on this
                instance yet.
        """
        if not self.parsed:
            raise FunctionNotParsed()

        if self.is_noop:
            return []

        if len(self.act_blocks) < 1:
            return [
                (self.node.lineno, self.node.col_offset, 'AAA01 no Act block found in test'),
            ]

        if len(self.act_blocks) > 1:
            return [
                (self.node.lineno, self.node.col_offset, 'AAA02 multiple Act blocks found in test'),
            ]

        return []
