import pytest

from flake8_aaa.act_block import ActBlock
from flake8_aaa.exceptions import ValidationError
from flake8_aaa.types import ActBlockType


@pytest.mark.parametrize('code_str', ['''
def test():
    result = 1

    assert result == 1
'''])
def test_assignment(function):
    result = function.load_act_block()

    assert isinstance(result, ActBlock)
    assert result.block_type == ActBlockType.result_assignment
    assert result.node.first_token.line == '    result = 1\n'


@pytest.mark.parametrize('code_str', ['''
def test():
    y = 3
    x = y + 1  # act
    assert x == 4
'''])
def test_act_marker(function):
    result = function.load_act_block()

    assert isinstance(result, ActBlock)
    assert result.block_type == ActBlockType.marked_act
    assert result.node.first_token.line == '    x = y + 1  # act\n'


@pytest.mark.parametrize(
    'code_str', [
        '''
def test(existing_user):
    result = existing_user.delete()

    assert result is True
    assert result.retrieved is False
    with pytest.raises(DoesNotExist):
        result.retrieve()
'''
    ]
)
def test_raises_in_assert(function):
    result = function.load_act_block()

    assert isinstance(result, ActBlock)
    assert result.block_type == ActBlockType.result_assignment
    assert result.node.first_token.line == '    result = existing_user.delete()\n'


# --- FAILURES ---


@pytest.mark.parametrize('code_str', ['''
def test():
    assert 1 + 1 == 2
'''])
def test_no_block(function):
    with pytest.raises(ValidationError) as excinfo:
        function.load_act_block()

    assert excinfo.value.line_number == 2
    assert excinfo.value.offset == 0
    assert excinfo.value.text == 'AAA01 no Act block found in test'


@pytest.mark.parametrize(
    'code_str', [
        '''
def test(user):
    result = login(user)  # Logging in User returns True
    assert result is True

    result = login(user)  # Already logged in User returns False
    assert result is False
    ''',
        '''
def test():
    chickens = 1  # act
    eggs = 1  # act

    assert chickens + eggs == 2
    ''',
    ]
)
def test_multiple_acts(function):
    with pytest.raises(ValidationError) as excinfo:
        function.load_act_block()

    assert excinfo.value.line_number == 2
    assert excinfo.value.offset == 0
    assert excinfo.value.text == 'AAA02 multiple Act blocks found in test'
