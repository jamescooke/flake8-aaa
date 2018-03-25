import tokenize
import io

import pytest

from flake8_aaa.helpers import load_markers


@pytest.fixture
def file_tokens(code_str):
    return list(tokenize.generate_tokens(io.StringIO(code_str).readline))


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

    assert list(result) == [2]
    assert result[2].string == '# aaa act'
