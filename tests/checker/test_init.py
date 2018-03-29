import ast

import pytest

from flake8_aaa import Checker


@pytest.mark.parametrize('code_str', ("""
def test():
    pass
""", ))
def test(code_str, file_tokens):
    tree = ast.parse(code_str)
    result = Checker(tree, '__FILENAME__', file_tokens)

    assert result.tree == tree
    assert result.filename == '__FILENAME__'
    assert result.file_tokens == file_tokens
    assert result.markers == {}
