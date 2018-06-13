from .act_block import ActBlock
from .exceptions import FunctionNotParsed, NotActionBlock
from .helpers import function_is_noop


class Function:
    """
    Attributes:
        act_blocks (list (ActBlock)): List of nodes that are considered Act
            blocks for this test. Defaults to ``None`` when function has not
            been parsed.
        is_noop (bool): Function is considered empty. Consists just of comments
            or ``pass``.
        lines (list (str)): Lines that make up this function. Extracted from
            the lines passed by Flake8.
        node (ast.FunctionDef): AST for the test under lint.
        parsed (bool): Function's nodes have been parsed.
    """

    def __init__(self, node, file_lines):
        """
        Args:
            node (ast.FunctionDef)
            file_lines (list (str)): Lines of file under test.
        """
        self.node = node
        self.act_blocks = []
        self.is_noop = False
        self.parsed = False
        self.lines = file_lines[self.node.lineno - 1:self.node.last_token.end[0]]

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

        for child_node in self.node.body:
            try:
                self.act_blocks.append(ActBlock.build(child_node))
            except NotActionBlock:
                continue

        # Allow `pytest.raises` in assert blocks
        if len(self.act_blocks) > 1:
            self.act_blocks = [self.act_blocks[0]] + list(
                filter(lambda ab: ab.block_type != ActBlock.PYTEST_RAISES, self.act_blocks[1:])
            )

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

    def get_line_relative_to_node(self, target_node, offset):
        """
        Args:
            target_node (ast.node)
            offset (int)

        Returns:
            str

        Raises:
            IndexError: when ``offset`` takes the request out of bounds of this
                Function's lines.
        """
        return self.lines[target_node.lineno - self.node.lineno + offset]
