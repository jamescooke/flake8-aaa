import pytest

from flake8_aaa.helpers import get_first_token, get_last_token


@pytest.mark.parametrize(
    'code_str', ['''
@unittest.skip('not today')
def test(self):
    self.fail('should not happen')
''']
)
def test_function_start(function):
    """
    Assert function fixture includes decorations
    """
    result = get_first_token(function.node).line

    assert result == "@unittest.skip('not today')\n"


@pytest.mark.parametrize(
    'code_str', ['''
@unittest.skip('not today')
def test(self):
    self.fail('should not happen')
''']
)
def test_function_end(function):
    """
    Assert function with decoractors continues through the whole function
    """
    result = get_last_token(function.node).line

    assert result == "    self.fail('should not happen')\n"
