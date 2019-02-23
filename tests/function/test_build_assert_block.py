import pytest

from flake8_aaa.block import Block
from flake8_aaa.types import LineType


@pytest.mark.parametrize(
    'code_str', ['''
def test():
    with pytest.raises(DoesNotExist):
        load_account(-1)
''']
)
def test_none(function_with_act_block):
    result = function_with_act_block.build_assert_block()

    assert result == 0
    assert isinstance(function_with_act_block.assert_block, Block)
    assert function_with_act_block.assert_block.nodes == ()
    assert function_with_act_block.assert_block.line_type == LineType.assert_block
    assert LineType.assert_block not in function_with_act_block.line_markers


@pytest.mark.parametrize(
    'code_str', [
        '''
def test():
    result = load_account(1)

    assert isinstance(result, Account)
    assert result.id == 1
''',
        '''
def test_raise(toy_instance):
    with pytest.raises(PlayError) as excinfo:
        toy_instance.run()

    assert 'Not ready' in excinfo.value.message
    assert toy_instance.has_run is False
''',
    ]
)
def test(function_with_act_block):
    result = function_with_act_block.build_assert_block()

    assert result == 2
    assert isinstance(function_with_act_block.assert_block, Block)
    assert len(function_with_act_block.assert_block.nodes) == 2
    assert function_with_act_block.line_markers[-2:] == [LineType.assert_block] * 2
