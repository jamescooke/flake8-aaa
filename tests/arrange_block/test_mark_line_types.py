import pytest

from flake8_aaa.arrange_block import ArrangeBlock
from flake8_aaa.types import LineType


@pytest.mark.parametrize(
    'code_str',
    ["""
def test():
    x = 1
    y = [
        2,
    ]

    result = [x] + y

    assert result == [1, 2]
"""]
)
def test(first_node_with_tokens):
    arrange_block = ArrangeBlock()
    arrange_block.add_node(first_node_with_tokens.body[0])
    arrange_block.add_node(first_node_with_tokens.body[1])
    line_types = [
        LineType.func_def,  # def test():
        LineType.unprocessed,  # x = 1
        LineType.unprocessed,  # y = [
        LineType.unprocessed,  # 2,
        LineType.unprocessed,  # ]
        LineType.unprocessed,  #
        LineType.act_block,  # result = [x] + y
        LineType.unprocessed,  #
        LineType.unprocessed,  # assert result == [1, 2]
    ]

    result = arrange_block.mark_line_types(line_types, 2)

    assert result == [
        LineType.func_def,  # def test():
        LineType.arrange_block,  # x = 1
        LineType.arrange_block,  # y = [
        LineType.arrange_block,  # 2,
        LineType.arrange_block,  # ]
        LineType.unprocessed,  #
        LineType.act_block,  # result = [x] + y
        LineType.unprocessed,  #
        LineType.unprocessed,  # assert result == [1, 2]
    ]
