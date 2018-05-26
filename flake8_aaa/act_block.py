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
    def build(obj, node):
        """
        Args:
            node (ast.node): A node, decorated with ``ASTTokens``.

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
        if node.first_token.line.strip().endswith('# act'):
            return obj(node, obj.MARKED_ACT)

        raise NotActionBlock()
