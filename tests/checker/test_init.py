import ast

import pytest

from flake8_aaa import Checker


@pytest.fixture
def ast_example() -> ast.AST:
    return ast.parse('pass')


# --- TESTS ---


def test(ast_example) -> None:
    result = Checker(ast_example, [], '__FILENAME__')

    assert result.tree == ast_example
    assert result.lines == []
    assert result.filename == '__FILENAME__'
    assert result.ast_tokens is None
