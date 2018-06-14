import pytest


@pytest.mark.parametrize(
    'code_str', [
        'def test():\n    pass',
        'def test_docstring():\n    """This test will work great"""',
    ]
)
def test_noop(function):
    function.parse()

    result = function.check()

    assert result == []


@pytest.mark.parametrize(
    'code_str', [
        '''
def test():
    result = 1

    assert result == 1
''',
        '''
def test(existing_user):
    result = existing_user.delete()

    assert result is True
    assert result.retrieved is False
    with pytest.raises(DoesNotExist):
        result.retrieve()
''',
    ]
)
def test_result_assigned(function):
    function.parse()

    result = function.check()

    assert result == []


@pytest.mark.parametrize('code_str', ['''
def test():
    assert 1 + 1 == 2
'''])
def test_no_result(function):
    function.parse()

    result = function.check()

    assert result == [
        # (line_number, offset, text)
        (2, 0, 'AAA01 no Act block found in test'),
    ]


@pytest.mark.parametrize('code_str', ['''
def test():
    x = 1 + 1  # act
    assert x == 2
'''])
def test_act(function):
    function.parse()

    result = function.check()

    assert result == []


@pytest.mark.parametrize(
    'code_str', [
        '''
def test(user):
    result = login(user)  # Logging in User returns True
    assert result is True

    result = login(user)  # Already logged in User returns False
    assert result is False
'''
    ]
)
def test_multi_act(function):
    function.parse()

    result = function.check()

    assert result == [
        # (line_number, offset, text)
        (2, 0, 'AAA02 multiple Act blocks found in test'),
    ]
