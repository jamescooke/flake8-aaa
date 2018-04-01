class ActBlock:
    """
    Attributes:
        node
        block_type (str)
    """

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
            node

        Returns:
            ActBlock

        Raises:
        """
        return obj(node, obj.RESULT_EQUALS)
