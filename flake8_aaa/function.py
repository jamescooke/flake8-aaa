from .act_block import ActBlock
from .exceptions import NotActionBlock, ValidationError
from .helpers import function_is_noop
from .types import ActBlockType


class Function:
    """
    Attributes:
        act_block (ActBlock): Act block for the test.
        node (ast.FunctionDef): AST for the test under lint.
    """

    def __init__(self, node):
        """
        Args:
            node (ast.FunctionDef)
        """
        self.node = node
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
