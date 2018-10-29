import pytest

from flake8_aaa.act_block import ActBlock
from flake8_aaa.types import LineType


@pytest.mark.parametrize(
    'code_str', [
        """
def test_not_actions(first_node_with_tokens):
    with pytest.raises(NotActionBlock):
        ActBlock.build(first_node_with_tokens)
"""
    ]
)
def test(first_node_with_tokens):
    act_block = ActBlock.build_body(first_node_with_tokens.body)[0]
    line_types = [LineType.func_def, LineType.unprocessed, LineType.unprocessed]

    result = act_block.mark_line_types(line_types, 2)

    assert result == [LineType.func_def, LineType.act_block, LineType.act_block]


@pytest.mark.parametrize(
    'code_str', [
        """



def test_add():
    x = 1
    y = 2

    result = x + y

    assert result == 3

# End
""",
    ]
)
def test_conflict(first_node_with_tokens):
    act_block = ActBlock.build_body(first_node_with_tokens.body)[0]
    line_types = [
        LineType.func_def,  # def test_add():
        LineType.unprocessed,  # x = 1
        LineType.unprocessed,  # y = 2
        LineType.unprocessed,  # [blank]
        LineType.func_def,  # result = x + y  # < sets up conflict
        LineType.unprocessed,  # [blank]
        LineType.unprocessed,  # assert result == 3
    ]

    with pytest.raises(AssertionError):
        act_block.mark_line_types(line_types, 5)
