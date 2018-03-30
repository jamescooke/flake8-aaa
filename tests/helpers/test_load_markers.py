import pytest

from flake8_aaa.helpers import load_markers


@pytest.mark.parametrize('code_str', [
    """
def test():
    assert True
""",
])
def test_none(file_tokens):
    result = load_markers(file_tokens)

    assert result == {}


@pytest.mark.parametrize('code_str', [
    """
def test():
    assert True  # aaa act
""",
])
def test_some(file_tokens):
    result = load_markers(file_tokens)

    assert list(result) == [3]
    assert result[3].token.string == '# aaa act'
