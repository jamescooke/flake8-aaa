from .exceptions import NotActionBlock
from .helpers import node_is_pytest_raises, node_is_result_assignment


class ActBlock:
    """
    Attributes:
        node
        block_type (str)
    """

    MARKED_ACT = 'marked_act'
    PYTEST_RAISES = 'pytest_raises'
    RESULT_ASSIGNMENT = 'result_assignment'

    def __init__(self, node, block_type):
        """
        Args:
            node
            block_type (str)
        """
        self.node = node
        self.block_type = block_type

    @classmethod
    def build(obj, node, tokens):
        """
        Args:
            node (astroid.*): An astroid node.
            tokens (asttokens.ASTTokens): Tokens that contain this node.

        Returns:
            ActBlock

        Raises:
            NotActionBlock: When ``node`` does not look like an Act block.
        """
        if node_is_result_assignment(node):
            return obj(node, obj.RESULT_ASSIGNMENT)
        elif node_is_pytest_raises(node):
            return obj(node, obj.PYTEST_RAISES)

        # Check if line marked with '# act'
        line = next(tokens.get_tokens(node, include_extra=True)).line
        if line.strip().lower().endswith('# act'):
            return obj(node, obj.MARKED_ACT)

        raise NotActionBlock()
