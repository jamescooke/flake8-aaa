import ast

import pytest

from flake8_aaa.helpers import function_is_noop


@pytest.mark.parametrize(
    'code_str', [
        '''
def test():
    pass
''',
        '''
def test_docstring():
    """This test will work great"""
''',
    ]
)
def test(code_str):
    node = ast.parse(code_str).body[0]

    result = function_is_noop(node)

    assert result is True


@pytest.mark.parametrize('code_str', [
    '''
def test_tomorrow():
    # FIX write this test
    result = 1
''',
])
def test_not_noop(code_str):
    node = ast.parse(code_str).body[0]

    result = function_is_noop(node)

    assert result is False
