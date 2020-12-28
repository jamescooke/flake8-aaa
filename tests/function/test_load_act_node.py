import pytest

from flake8_aaa.act_node import ActNode
from flake8_aaa.exceptions import ValidationError
from flake8_aaa.types import ActNodeType


@pytest.mark.parametrize('code_str', ['''
def test():
    result = 1

    assert result == 1
'''])
def test_assignment(function):
    result = function.load_act_node()

    assert isinstance(result, ActNode)
    assert result.block_type == ActNodeType.result_assignment
    assert result.node.first_token.line == '    result = 1\n'


@pytest.mark.parametrize('code_str', ['''
def test():
    y = 3
    x = y + 1  # act
    assert x == 4
'''])
def test_act_marker(function):
    result = function.load_act_node()

    assert isinstance(result, ActNode)
    assert result.block_type == ActNodeType.marked_act
    assert result.node.first_token.line == '    x = y + 1  # act\n'


@pytest.mark.parametrize('code_str', ['''
def test():
    y = 3
    x = y + 1  # Act
    assert x == 4
'''])
def test_act_marker_case(function):
    """
    Act marker is case-insensitive
    """
    result = function.load_act_node()

    assert isinstance(result, ActNode)
    assert result.block_type == ActNodeType.marked_act
    assert result.node.first_token.line == '    x = y + 1  # Act\n'


@pytest.mark.parametrize(
    'code_str',
    [
        '''
def test(existing_user):
    result = existing_user.delete()

    assert result is True
    assert result.retrieved is False
    with pytest.raises(DoesNotExist):
        result.retrieve()
''',
        '''
def test(self):
    existing_user = self.get_user()

    result = existing_user.delete()

    self.assertIs(result, True)
    self.assertIs(result.retrieved, False)
    with self.assertRaises(DoesNotExist):
        result.retrieve()
''',
    ],
    ids=['pytest raises in Assert', 'unittest raises in Assert'],
)
def test_raises_in_assert(function):
    result = function.load_act_node()

    assert isinstance(result, ActNode)
    assert result.block_type == ActNodeType.result_assignment
    assert result.node.first_token.line == '    result = existing_user.delete()\n'


@pytest.mark.parametrize(
    'code_str',
    [
        '''
def test(existing_user):
    with mock.patch('stats.deletion_manager.deleted'):
        result = existing_user.delete()

    assert result is True
    assert result.retrieved is False
'''
    ],
    ids=['act in context manager'],
)
def test_in_cm(function):
    result = function.load_act_node()

    assert isinstance(result, ActNode)
    assert result.block_type == ActNodeType.result_assignment
    assert result.node.first_token.line == '        result = existing_user.delete()\n'


@pytest.mark.parametrize(
    'code_str',
    [
        '''
def test_no_recreate(existing_user):
    with mock.patch('stats.creation_manager.created'):
        with pytest.raises(ValidationError):
            existing_user.create()
'''
    ],
    ids=['pytest raises in context manager'],
)
def test_raises_in_cm(function):
    result = function.load_act_node()

    assert isinstance(result, ActNode)
    assert result.block_type == ActNodeType.pytest_raises
    assert result.node.first_token.line == '        with pytest.raises(ValidationError):\n'


@pytest.mark.parametrize(
    'code_str',
    [
        '''
def test_creation(stub_user):
    with mock.patch('stats.creation_manager.created'):
        stub_user.create()  # act

    assert stub_user.exists()
'''
    ],
    ids=['marked act block in context manager'],
)
def test_marked_in_cm(function):
    result = function.load_act_node()

    assert isinstance(result, ActNode)
    assert result.block_type == ActNodeType.marked_act
    assert result.node.first_token.line == '        stub_user.create()  # act\n'


# --- FAILURES ---


@pytest.mark.parametrize('code_str', ['''
def test():
    assert 1 + 1 == 2
'''])
def test_no_block(function):
    with pytest.raises(ValidationError) as excinfo:
        function.load_act_node()

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
        '''
def test_read(self):
    with open('data') as data_file:
        result = data_file.read()

        assert result == ''

        result = data_file.read()

        assert result == ''
    ''',
    ]
)
def test_multiple_acts(function):
    with pytest.raises(ValidationError) as excinfo:
        function.load_act_node()

    assert excinfo.value.line_number == 2
    assert excinfo.value.offset == 0
    assert excinfo.value.text == 'AAA02 multiple Act blocks found in test'
