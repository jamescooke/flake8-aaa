import pytest


@pytest.mark.parametrize('code_str', ['''
def test():
    result = 1

    assert result == 1
'''])
def test(function_with_arrange_act_blocks):
    result = function_with_arrange_act_blocks.check_act_arrange_spacing()

    assert result is None
