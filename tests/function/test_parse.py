import pytest


@pytest.mark.parametrize('code_str', ['def test():\n    pass'])
def test_none(function):
    result = function.parse()

    assert result == 0
    assert function.act_blocks == []


@pytest.mark.parametrize('code_str', ['def test():\n    result = 1\n\n    assert result is 1'])
def test_one(function):
    result = function.parse()

    assert result == 1


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
def test_multi(function):
    result = function.parse()

    assert result == 2
