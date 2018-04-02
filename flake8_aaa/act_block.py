from .helpers import node_is_pytest_raises, node_is_result_equals


class ActBlock:
    """
    Attributes:
        node
        block_type (str)
    """

    PYTEST_RAISES = 'pytest_raises'
    RESULT_EQUALS = 'result_equals'

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
            node: An ``ast`` node.

        Returns:
            ActBlock

        Raises:
        """
        if node_is_result_equals(node):
            return obj(node, obj.RESULT_EQUALS)
        elif node_is_pytest_raises(node):
            return obj(node, obj.PYTEST_RAISES)
