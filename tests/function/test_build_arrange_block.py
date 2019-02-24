import pytest

from flake8_aaa.block import Block
from flake8_aaa.types import LineType


@pytest.mark.parametrize('code_str', ['''
def test():
    result = 1

    assert result == 1
'''])
def test_none(function_with_act_block):
    result = function_with_act_block.build_arrange_block()

    assert result == 0
    assert isinstance(function_with_act_block.arrange_block, Block)
    assert function_with_act_block.arrange_block.line_type == LineType.arrange_block
    assert function_with_act_block.arrange_block.nodes == ()
    assert LineType.arrange_block not in function_with_act_block.line_markers


@pytest.mark.parametrize(
    'code_str', ['''
def test():
    x = 1
    y = 1

    result = x + y

    assert result == 2
''']
)
def test_simple(function_with_act_block):
    result = function_with_act_block.build_arrange_block()

    assert result == 2
    assert isinstance(function_with_act_block.arrange_block, Block)
    assert function_with_act_block.arrange_block.line_type == LineType.arrange_block
    assert len(function_with_act_block.arrange_block.nodes) == 2
    assert function_with_act_block.line_markers[1:3] == [LineType.arrange_block] * 2


@pytest.mark.parametrize(
    'code_str', [
        '''
def test():
    """
    Simple test
    """
    x = 1
    y = 1

    result = x + y

    assert result == 2
'''
    ]
)
def test_filtered(function_with_act_block):
    result = function_with_act_block.build_arrange_block()

    assert result == 2
    assert isinstance(function_with_act_block.arrange_block, Block)
    assert function_with_act_block.arrange_block.line_type == LineType.arrange_block
    assert len(function_with_act_block.arrange_block.nodes) == 2
    assert function_with_act_block.line_markers[4:6] == [LineType.arrange_block] * 2
