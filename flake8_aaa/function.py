from .act_block import ActBlock
from .arrange_block import ArrangeBlock
from .assert_block import AssertBlock
from .exceptions import NotActionBlock, ValidationError
from .helpers import function_is_noop
from .types import ActBlockType


class Function:
    """
    Attributes:
        act_block (ActBlock): Act block for the test.
        node (ast.FunctionDef): AST for the test under lint.
    """

    def __init__(self, node, file_lines):
        """
        Args:
            node (ast.FunctionDef)
            file_lines (list (str)): Lines of file under test.
        """
        self.node = node
        self.lines = file_lines[self.node.lineno - 1:self.node.last_token.end[0]]
        self.act_block = None

    def check_all(self):
        """
        Run everything required for checking this function.

        Returns:
            None: On success.

        Raises:
            ValidationError: When an error is found.
        """
        if function_is_noop(self.node):
            return

        self.act_block = self.load_act_block()
        self.arrange_block = self.load_arrange_block()
        self.check_arrange_act_spacing()
        self.assert_block = self.load_assert_block()
        self.check_act_assert_spacing()

    def load_act_block(self):
        """
        Returns:
            ActBlock

        Raises:
            ValidationError
        """
        act_blocks = []
        for child_node in self.node.body:
            try:
                act_blocks.append(ActBlock.build(child_node))
            except NotActionBlock:
                continue

        # Allow `pytest.raises` in assert blocks - ignore all act blocks that
        # are `pytest.raises` blocks that are not the first.
        if len(act_blocks) > 1:
            act_blocks = [act_blocks[0]
                          ] + list(filter(lambda ab: ab.block_type != ActBlockType.pytest_raises, act_blocks[1:]))

        if len(act_blocks) < 1:
            raise ValidationError(self.node.lineno, self.node.col_offset, 'AAA01 no Act block found in test')
        if len(act_blocks) > 1:
            raise ValidationError(self.node.lineno, self.node.col_offset, 'AAA02 multiple Act blocks found in test')

        return act_blocks[0]

    def load_arrange_block(self):
        """
        Returns:
            ArrangeBlock: Or ``None`` if no Act block is found.
        """
        arrange_block = ArrangeBlock()
        for node in self.node.body:
            if node == self.act_block.node:
                break
            arrange_block.add_node(node)

        if len(arrange_block.nodes) > 0:
            return arrange_block

        return None

    def load_assert_block(self):
        """
        Returns:
            AssertBlock: Or ``None`` if no Assert block is found.
        """
        assert_block = AssertBlock()
        for node in self.node.body:
            if node.lineno > self.act_block.node.lineno:
                assert_block.add_node(node)

        if len(assert_block.nodes) > 0:
            return assert_block

        return None

    def check_arrange_act_spacing(self):
        """
        When Function has an Arrange block, then ensure that there is a blank
        line between that and the Act block.

        Returns:
            None

        Raises:
            ValidationError: When no space found.

        Note:
            Due to Flake8's error ``E303``, we do not have to check that there
            is more than one space.
        """
        if self.arrange_block:
            line_before_act = self.get_line_relative_to_node(self.act_block.node, -1)
            if line_before_act != '\n':
                raise ValidationError(
                    line_number=self.act_block.node.lineno,
                    offset=self.act_block.node.col_offset,
                    text='AAA03 expected 1 blank line before Act block, found none',
                )

    def check_act_assert_spacing(self):
        """
        Raises:
            ValidationError: When no space found
        """
        if self.assert_block:
            line_before_assert = self.get_line_relative_to_node(self.assert_block.nodes[0], -1)
            if line_before_assert != '\n':
                raise ValidationError(
                    line_number=self.assert_block.nodes[0].lineno,
                    offset=self.assert_block.nodes[0].col_offset,
                    text='AAA04 expected 1 blank line before Assert block, found none',
                )

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
