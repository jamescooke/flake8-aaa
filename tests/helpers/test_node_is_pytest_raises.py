import astroid
import pytest

from flake8_aaa.helpers import node_is_pytest_raises


@pytest.mark.parametrize(
    'code_str', [
        '''with pytest.raises(Exception):
    do_thing()''', '''with pytest.raises(Exception) as excinfo:
    do_thing()'''
    ]
)
def test(code_str):
    node = astroid.parse(code_str).body[0]

    result = node_is_pytest_raises(node)

    assert result is True


@pytest.mark.parametrize('code_str', [
    '''with open('test.txt') as f:
    f.read()''',
])
def test_no(code_str):
    node = astroid.parse(code_str).body[0]

    result = node_is_pytest_raises(node)

    assert result is False
