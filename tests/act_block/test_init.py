import ast

from flake8_aaa.act_block import ActBlock


def test():
    node = ast.parse('result = do_thing()').body[0]

    result = ActBlock(node, 'result_equals')

    assert result.node == node
    assert result.block_type == ActBlock.RESULT_EQUALS
