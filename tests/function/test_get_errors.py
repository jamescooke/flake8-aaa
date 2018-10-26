import pytest


@pytest.mark.parametrize('code_str', ['def test():\n    pass'])
def test_noop(function):
    result = function.get_errors()

    assert result == []


@pytest.mark.parametrize(
    'code_str', [
        '''
def test(file_resource):
    file_resource.connect()
    result = file_resource.retrieve()

    assert result.success is True
''',
    ]
)
def test_one(function):
    result = function.get_errors()

    assert len(result) == 1
    assert result[0][0] == 4
    assert result[0][1] == 4
    assert result[0][2].startswith('AAA03 ')
    assert result[0][3] is type(function)
