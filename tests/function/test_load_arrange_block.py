import pytest

from flake8_aaa.arrange_block import ArrangeBlock


@pytest.mark.parametrize('code_str', ['''
def test():
    result = 1

    assert result == 1
'''])
def test_none(function_with_act_block):
    function_with_act_block.load_act_block()

    result = function_with_act_block.load_arrange_block()

    assert result is None


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
    function_with_act_block.load_act_block()

    result = function_with_act_block.load_arrange_block()

    assert isinstance(result, ArrangeBlock)
